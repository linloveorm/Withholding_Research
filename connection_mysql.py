import mysql.connector


cnx = mysql.connector.connect(user='root', password='keep1234',host='192.168.99.100',database='keeplearning')

cursor = cnx.cursor(buffered=True)

query = ("""SELECT TypeOfIncome, IncomeTaxAssessable
        FROM IncomeAssessable
        WHERE IncomeTaxAssessable = '40(1)' """)


cursor.execute(query)
records = cursor.fetchall()

print(records)


cursor.close()
cnx.close()