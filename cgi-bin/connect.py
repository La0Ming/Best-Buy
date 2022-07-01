import mysql.connector as mysql
import var

connection = mysql.connect(user=var.MYSQL_USER,
                           passwd=var.MYSQL_PASS,
                           database=var.MYSQL_DATABASE, 
                           host='127.0.0.1')


cnx = connection.cursor(dictionary=True)
print('Connect')
cnx.execute('''SELECT * FROM Customers''')
for row in cnx:
    print(row)
cnx.execute('''SELECT * FROM Orders''')
for row in cnx:
    print(row)

connection.close()