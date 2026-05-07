import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

server = 'KUBALAPTOP'
database = 'CyberTrainer'

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
params = quote_plus(conn_str)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

