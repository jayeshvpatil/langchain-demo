import pymssql

server = 'localhost' 
database = 'demodb' 
username = 'sa' 
password = 'p@55word' 
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.

conn = pymssql.connect(server, user=username, password=password, database='demodb')
cursor = conn.cursor()  
cursor.execute('SELECT top 10 * FROM sales.customer')  
row = cursor.fetchone()  
while row:  
    print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))     
    row = cursor.fetchone()  