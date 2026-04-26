import pyodbc

server = 'KUBALAPTOP'
database = 'CyberTrainer'

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("select nickname from users JOIN Gender ON GenderID = IDGender JOIN Advancement ON AdvancementID = IDAdvancement WHERE GenderName = 'Mężczyzna'")
    tables = cursor.fetchall()

    for table in tables:
        print(table[0])

    conn.close()
except pyodbc.Error as e:
    print(e)