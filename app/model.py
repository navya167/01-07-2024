from sqlalchemy import Column, Integer, Text, create_engine , ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

class ExpenseTracker(Base):
    __tablename__ = "expense_tracker"
    id = Column(Integer, primary_key=True)
    expenditure_details  = Column(Text)
    expenditure_transaction = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    date = Column(Date, nullable=False) 
    user = relationship("User", back_populates="finance_tracker")
    
    def __init__(self, expenditure_details, expenditure_transaction, user_id, date):
        self.expenditure_details = expenditure_details
        self.expenditure_transaction = expenditure_transaction
        self.user_id = user_id
        self.date = date

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text, unique=True)
    password = Column(Text)
    finance_tracker = relationship("ExpenseTracker", back_populates="user", cascade="all, delete-orphan")
    is_active = Column(Boolean, default=True)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        

        
# Step 1: Define the connection string
DATABASE_URL = "postgresql://<username>:<password>@localhost/<dbname>"  # Replace with your actual database URL
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

session.commit()

    