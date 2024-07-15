from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from service import Login, TrackExpense  # Import your service methods

app = Flask(__name__)
app.secret_key = '123'  # Set your secret key for session management

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Mock User model for demonstration (replace with your actual User model)
class User:
    def __init__(self, id):
        self.id = id
        self.is_active = True
        
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    # Implementing the required methods from UserMixin
    def get_id(self):
        return str(self.id)

# Mock function to load user (replace with your actual user loading logic)
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def load_default():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def load_dashboard():
    user_id = current_user.id
    return render_template('dashboard.html', user_id=user_id)

@app.route('/register_form')
def register_form():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    login_instance = Login()
    data = request.form
    username = data.get('username')
    password = data.get('password')
    user = login_instance.validate_user(username, password)
    
    if user:
        login_user(User(user.id))  # Log in the user
        return redirect(url_for('load_dashboard'))
    else:
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('load_default'))
    
@app.route('/register', methods=['POST'])
def register():
    login_instance = Login()
    data = request.form
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    result = login_instance.create_user(username, password, email)
    
    if result:
        flash('User created successfully. Please log in.')
        return redirect(url_for('load_default'))
    else:
        flash('User already exists. Please use a different email.')
        return redirect(url_for('register_form'))

@app.route('/filtered', methods=['POST'])
@login_required
def get_expense_data():
    instance = TrackExpense()
    user_id = current_user.id
    date_from = request.json.get('dateFrom')  # Adjust according to your form data
    date_to = request.json.get('dateTo')      # Adjust according to your form data
    expenses = instance.get_all_tracker_detail(user_id, date_from, date_to)
    formatted_expenses = []
    for expense in expenses:
        formatted_expense = {
            'id': expense.id,
            'date': expense.date.strftime("%a, %d %b %Y"),  # Format date as required
            'expenditure_details': expense.expenditure_details,
            'expenditure_transaction': expense.expenditure_transaction
        }
        formatted_expenses.append(formatted_expense)

    return jsonify(formatted_expenses)

@app.route('/api/add_expense', methods=['POST'])
@login_required
def api_add_expense():
    data = request.get_json()
    user_id = current_user.id
    expenditure_details = data.get('expenditure_details')
    expenditure_transaction = data.get('expenditure_transaction')
    date = data.get('expenditure_date')
    instance = TrackExpense()
    
    if not expenditure_details or not expenditure_transaction or not date:
        return jsonify(success=False, message="All fields are required"), 400
    
    try:
        success = instance.add_tracker_data(user_id, expenditure_details, expenditure_transaction, date)
        if success:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Failed to add expense"), 500
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500
    
    
@app.route('/api/get_expenses/<user_id>', methods=['GET'])
def get_expenses(user_id):
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    instance = TrackExpense()
    expenses = instance.get_all_tracker_detail(user_id, date_from, date_to)

    formatted_expenses = []
    for expense in expenses:
        formatted_expense = {
            'id': expense.id,
            'date': expense.date.strftime("%a, %d %b %Y"),  # Format date as required
            'expenditure_details': expense.expenditure_details,
            'expenditure_transaction': expense.expenditure_transaction
        }
        formatted_expenses.append(formatted_expense)

    return jsonify(formatted_expenses)

if __name__ == '__main__':
    app.run()
