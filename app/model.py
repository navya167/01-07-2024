from sqlalchemy import Column, Integer, Text, create_engine , ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

class User(Base):
    __tablename__  = "user"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text, unique= True)
    password =  Column(Text)
    finance_tracker = relationship("FinanceTracker", back_populates = "user", cascade = "all")
    def __init__(self, name, email, password) -> None:
        self.name = name
        self.email = email
        self.password = password
        
        
        
class FinanceTracker:
    __tablename__  = "finance_tracker"
    id = Column(Integer, primary_key=True)
    category = Column(Text)
    item = Column(Text)
    description =  Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="finance_tracker")

       
        
# Step 1: Define the connection string
DATABASE_URL = "postgresql://<username>:<password>@localhost/<dbname>"  # Replace with your actual database URL
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

session.commit()

    