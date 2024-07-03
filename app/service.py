from model import User, session
from sqlalchemy.exc import IntegrityError


class Login:
    def __init__(self) -> None:
        self.session = session
        pass
    
    def create_user(self, user_name, password, email):
        try:
            user_obj = User(name=user_name,
                password= password,
                email = email)
            session.add(user_obj)
            session.commit()
        except IntegrityError  as e:
            raise ValueError('Entered email already exist Please enter a different email address')
        except Exception as e:
            print(e)
    
    def update_user(self, user_id, name, email, password):
        try:
            session.query(User).filter_by(id=user_id).update({'name': name,'email': email, 'password': password })
            session.commit()
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

user_name = input('Enter your name: ') 
password = input('Enter your password: ')
email = input('Enter your email address: ')           
login = Login()
login.create_user(user_name, password, email)
# # login.update_user(1,'navya.s','navya.s@gmail.com', 'test123222')
# login.delete_user(1)


class Tracker:
    def __init__(self) -> None:
        self.session = session
        
    def add_tracker_data(self, user_id, item_name, date, amount_spent):
        pass