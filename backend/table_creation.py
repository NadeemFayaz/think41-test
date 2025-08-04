from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the database connection
engine = create_engine('sqlite:///example.db')
Base = declarative_base()

# User Table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    age = Column(Integer)
    gender = Column(String)
    state = Column(String)
    street_adress = Column(String)
    postal_code = Column(String)
    city = Column(String)
    country = Column(String)
    latitude = Column(Integer)
    longitude = Column(Integer)
    traffic_source = Column(String)

# Create tables 
Base.metadata.create_all(engine)

# Insert and verify
Session = sessionmaker(bind=engine)
session = Session()

# Add a sample user
new_user = User(first_name='Nadeem', email='nad@123.com')
session.add(new_user)
session.commit()

# Query
for u in session.query(User).all():
    print(f'User: {u.first_name}')