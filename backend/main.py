import pandas as pd
from sqlalchemy import create_engine

#crete a database connection
engine = create_engine('sqlite:///example.db')

#laod data from a CSV file
data = pd.read_csv('./data/users.csv')

#load to database
data.to_sql('data_table', con=engine, if_exists='replace', index=False)

#verify the data was loaded
print(pd.read_sql('SELECT * FROM data_table', con=engine))