# Expense Tracker Application Changes

## 1. Security Enhancements
1. Implemented CSRF protection to prevent cross-site request forgery attacks.
2. Utilized a `.env` file to securely store environment variables and secret keys.
3. Enabled password hashing to securely store user credentials.
4. Added an audit trail for currency conversions to ensure transparency and accountability.

## 2. Assumptions and Changes Made
1. The "Submit New Expense" button required a POST method. Added necessary input fields in `dashboard.html` to support this functionality.
2. The "Submit Expense" button in `base.html` was incorrectly calling the `/submit_expense` POST method directly. Created a `submit_expense_form` API (GET method) to render the `submit_expense.html` template correctly.
3. The `submit_expense.html` template was missing the `action="{{ url_for('submit_expense') }}"` attribute for the POST method. This was added to ensure proper form submission.
4. Added CSRF tokens to all HTML forms to enhance security.
5. Updated the `expense_detail.html` template to display the converted USD amount.
6. Modified the `convert_to_usd` function in `fx_service.py` to calculate USD rates via EUR, ensuring accurate cross-currency conversions.
7. Implemented basic error handling. Detailed error messages are still pending for future improvements.
8.`requirements.txt` file also i chamge sqlalchemy version `SQLAlchemy==2.0.21`  version because of python compatibility issue.

