from model import ExpenseTracker, User, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_


class Login:
    def __init__(self) -> None:
        self.session = session
    
    def create_user(self, user_name, password, email):
        try:
            user = self.session.query(User).filter_by(email=email).first()
            if user:
                return False  # User already exists
            user_obj = User(name=user_name, password=password, email=email)
            self.session.add(user_obj)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False
        except Exception as e:
            print(e)
            self.session.rollback()
            return False

    def validate_user(self, user_name, password):
        try:
            user = self.session.query(User).filter_by(name=user_name, password=password).first()
            if user:
                return user
            return False
        except Exception as e:
            print(e)
            return False
    
    def update_user(self, user_id, name, email, password):
        try:
            session.query(User).filter_by(id=user_id).update({'name': name,'email': email, 'password': password })
            session.commit()
            return True
        except IntegrityError  as e:
            raise ValueError('Entered email already exist Please enter a different email address')
        except Exception as e:
            print(e)
        
    def delete_user(self, user_id):
        try:
            session.query(User).filter_by(id = user_id).delete()
            session.commit()
        except Exception as e:
            print(e)

# user_name = input('Enter your name: ') 
# password = input('Enter your password: ')
# email = input('Enter your email address: ')           
# login = Login()
# login.create_user(user_name, password, email)
# # login.update_user(1,'navya.s','navya.s@gmail.com', 'test123222')
# login.delete_user(1)


class TrackExpense:
    def __init__(self) -> None:
        self.session = session
        
    def add_tracker_data(self, user_id, expenditure_details, expenditure_transaction, date):
        try:
            obj = ExpenseTracker(user_id= user_id, expenditure_details = expenditure_details, expenditure_transaction = expenditure_transaction, date = date)
            session.add(obj)
            session.commit()
            return True
        except Exception as e:
            print(e)
            
    def get_all_tracker_detail(self, user_id, date_from=None, date_to=None):
        try:
            query = self.session.query(ExpenseTracker.expenditure_details, ExpenseTracker.id, ExpenseTracker.expenditure_transaction, ExpenseTracker.date)
            query = query.filter(ExpenseTracker.user_id == user_id)
            
            if date_from and date_to:
                query = query.filter(and_(ExpenseTracker.date >= date_from, ExpenseTracker.date <= date_to))
            
            results = query.all()
            return results  # Return SQLAlchemy query results directly
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return {"status": "error", "message": str(e)}
    
    def update_expense_data(self, expense_id, expenditure_details, expenditure_transaction, date):
        try:
            session.query(ExpenseTracker).filter_by(id=expense_id).update({'expenditure_details': expenditure_details,'expenditure_transaction': expenditure_transaction, 
                                                                           'date': date })
            session.commit()
            return True
        except Exception as e:
            print(e)
            
    def delete_expense_data(self, expense_id):
        try:
            session.query(User).filter_by(id = expense_id).delete() 
            session.commit()
        except Exception as e:
            print(e)
            
def convert_obj_to_jsonify(obj):
    result_dict = []
    if obj != None:
        result_dict = [dict(row) for row in obj]
    return result_dict