import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from sqlalchemy import text
server = 'KUBALAPTOP'
database = 'CyberTrainer'

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
params = quote_plus(conn_str)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Połączenie udane!")
except Exception as e:
    print("Błąd połączenia:", e)
