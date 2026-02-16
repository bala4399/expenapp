from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='employee')
    department = db.Column(db.String(50), nullable=False, default='General')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    amount_original = db.Column(db.Float, nullable=False)
    currency_original = db.Column(db.String(3), nullable=False)
    amount_usd = db.Column(db.Float, nullable=False)

    description = db.Column(db.String(500), nullable=False)
    expense_date = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(20), default='pending')
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    approval_date = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FXConversionAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))

    original_amount = db.Column(db.Float, nullable=False)
    original_currency = db.Column(db.String(3), nullable=False)
    converted_amount_usd = db.Column(db.Float, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)

    rate_date = db.Column(db.String(8))
    source = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)