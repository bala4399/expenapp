import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Expense, Category, FXConversionAudit
from fx_service import convert_to_usd
from datetime import date, datetime
from functools import wraps
import os
from flask_wtf.csrf import CSRFProtect
  
app = Flask(__name__)
# if not os.getenv("SECRET_KEY"):
#     raise RuntimeError("SECRET_KEY not set")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev_only_key")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize CSRF protection
csrf = CSRFProtect(app)

db.init_app(app)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# def admin_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if 'user_id' not in session:
#             flash('Admin access required.')
#             return redirect(url_for('login'))
#         # user = User.query.get(session['user_id'])
#         return f(*args, **kwargs)
#     return wrapper

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        session.clear()
        session['user_id'] = user.id
        session['role'] = user.role
        flash("Login successful")
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid username or password")
        return redirect(url_for('index'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
        
#         if User.query.filter_by(username=username).first():
#             flash("Username already exists")
#             return redirect(url_for('register'))
        
#         user = User(username=username, email=email)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
        
#         flash("Registration successful. Please login.")
#         return redirect(url_for('index'))
    
#     return render_template('register.html')

def get_related_data(expenses):
    expense_data = []
    for expense in expenses:
        category = Category.query.get(expense.category_id)
        category_name = category.name if category else 'Unknown'
        user = User.query.get(expense.user_id)
        user_name = user.username if user else 'Unknown'
        expense_data.append({
            'expense': expense,
            'category_name': category_name,
            'user_name': user_name
        })
    return expense_data

@app.route('/dashboard')
@login_required
def dashboard():
    search_query = request.args.get('search', '')
    
    if session['role'] == 'admin':
        # Admin sees all expenses
        if search_query:
            expenses = Expense.query.filter(
                Expense.description.contains(search_query) |
                Expense.amount_original.like(f"%{search_query}%")
            ).all()
        else:
            expenses = Expense.query.all()
    else:
        # Regular users see only their own expenses
        if search_query:
            expenses = Expense.query.filter_by(user_id=session['user_id']).filter(
                Expense.description.contains(search_query)
            ).all()
        else:
            expenses = Expense.query.filter_by(user_id=session['user_id']).all()

    expense_data = get_related_data(expenses)

    # Calculate totals
    total_pending = sum(e['expense'].amount_original for e in expense_data if e['expense'].status == 'pending')
    total_approved = sum(e['expense'].amount_original for e in expense_data if e['expense'].status == 'approved')

    return render_template('dashboard.html', 
                           expense_data=expense_data,
                           total_pending=total_pending,
                           total_approved=total_approved,
                           search_query=search_query)

@app.route('/expense/<int:expense_id>')
@login_required
def expense_detail(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    category = Category.query.get(expense.category_id)
    user = User.query.get(expense.user_id)
    
    return render_template('expense_detail.html', 
                         expense=expense, 
                         category=category,
                         user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for('index'))

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access required")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return wrapper

@app.route('/submit_expense', methods=['POST'])
@login_required
def submit_expense():# Redirect GET requests to the dashboard

    # Handle POST requests
    expense_date = request.form.get('expense_date')
    amount = float(request.form['amount'])
    currency = request.form['currency']
    category_id = int(request.form['category_id'])
    description = request.form['description']

    # Validate required fields
    if 'expense_date' not in request.form or not request.form['expense_date']:
        flash("Expense date is required.")
        return redirect(url_for('dashboard'))

    expense_date = datetime.strptime(request.form['expense_date'], "%Y-%m-%d").date()

    usd_amount, fx_rate = convert_to_usd(amount, currency)

    expense = Expense(
        user_id=session['user_id'],
        category_id=category_id,
        amount_original=amount,
        currency_original=currency,
        amount_usd=usd_amount,
        description=description,
        expense_date=expense_date
    )

    db.session.add(expense)
    db.session.flush()

    audit = FXConversionAudit(
        expense_id=expense.id,
        original_amount=amount,
        original_currency=currency,
        converted_amount_usd=usd_amount,
        exchange_rate=fx_rate,
        rate_date="20250701",
        source="Mock FX API"
    )

    db.session.add(audit)
    db.session.commit()

    flash("Expense submitted successfully")
    return redirect(url_for('dashboard'))

@app.route('/approve_expense/<int:expense_id>')
@admin_required
def approve_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    expense.status = 'approved'
    expense.approved_by = session['user_id']
    expense.approval_date = datetime.utcnow()
    
    db.session.commit()
    flash('Expense approved successfully')
    return redirect(url_for('dashboard'))

@app.route('/deny_expense/<int:expense_id>')
@admin_required
def deny_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    expense.status = 'rejected'
    expense.approved_by = session['user_id']
    expense.approval_date = datetime.utcnow()
    
    db.session.commit()
    flash('Expense denied')
    return redirect(url_for('dashboard'))

@app.route('/submit_expense_form', methods=['GET'])
@login_required
def submit_expense_form():
    categories = Category.query.all()
    return render_template('submit_expense.html', categories=categories)

def init_db():
    """Initialize database with sample data. This code is not part of the interview task."""
    with app.app_context():
        # Drop all tables and recreate them to ensure clean state
        db.drop_all()
        db.create_all()
        
        # Create sample users
        admin = User(username='admin', email='admin@company.com', role='admin', department='IT')
        admin.set_password('admin123')
        
        employee1 = User(username='john', email='john@company.com', role='employee', department='Sales')
        employee1.set_password('john123')
        
        employee2 = User(username='jane', email='jane@company.com', role='employee', department='Marketing')
        employee2.set_password('jane123')
        
        db.session.add_all([admin, employee1, employee2])
        db.session.commit()  # Commit users first
        
        # Create expense categories
        categories = [
            Category(name='Travel', description='Business travel expenses'),
            Category(name='Meals', description='Business meal expenses'),
            Category(name='Office Supplies', description='Office equipment and supplies'),
            Category(name='Training', description='Professional development'),
        ]
        
        db.session.add_all(categories)
        db.session.commit()  # Commit categories before creating expenses
        
        # Create sample expenses
        import random
        users = User.query.filter(User.role == 'employee').all()
        categories_list = Category.query.all()
        
        for user in users:
            for i in range(random.randint(3, 6)):
                expense = Expense(
                    user_id=user.id,
                    category_id=random.choice(categories_list).id,
                    amount_original=round(random.uniform(25.0, 500.0), 2),
                    currency_original="USD",
                    amount_usd=round(random.uniform(25.0, 500.0), 2),
                    description=f"Sample expense {i+1} for {user.username}",
                    expense_date=date(2023, random.randint(1, 12), random.randint(1, 28)),
                    status=random.choice(['pending', 'approved', 'rejected'])
                )
                db.session.add(expense)
        
        db.session.commit()
        print("Database initialized with sample data!")



if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=True)