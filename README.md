# Expense Tracker - Technical Interview Sample App

## Quick Start

1. **Create and activate a virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your browser to `http://localhost:5000`

## Core Features

### For All Users
- **Dashboard:** View expenses with integrated search functionality
- **Submit Expense:** Create new expense claims
- **View Details:** See individual expense information

### For Employees
- See only their own expense claims
- Submit new expense claims
- Search through their own expenses

### For Admins
- See all expense claims from all employees
- Approve or deny pending expense claims
- Search through all expenses in the system

## Database Models

The application uses SQLite with three simple models:
- `User` - Application users with roles (admin/employee) and departments
- `Expense` - Individual expense records with approval workflow
- `Category` - Expense categories (Travel, Meals, Office Supplies, Training)


**⚠️ IMPORTANT:** This application contains intentional security vulnerabilities and performance issues for educational purposes. Do not use in production environments. 
