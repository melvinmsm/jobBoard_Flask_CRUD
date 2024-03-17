from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL configuration
mydb=mysql.connector.connect(
    host="sql3.freemysqlhosting.net",
    user="sql3691930",
    passwd="9e8XfLBmW5",
    db="sql3691930"
)
 
my_cursor=mydb.cursor()
my_cursor.execute("""
         CREATE TABLE IF NOT EXISTS JobBoard (
             jobID INT AUTO_INCREMENT PRIMARY KEY,
             jobName VARCHAR(255) NOT NULL,
             jobDescription VARCHAR(255) NOT NULL,
             postingDate DATE NOT NULL,
             location VARCHAR(255) NOT NULL
         )
     """)
my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)



if __name__ == '__main__':
    app.run(debug=True)
