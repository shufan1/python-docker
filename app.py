from flask import Flask
from flask import render_template
import mysql.connector
import json
import numpy as np

app = Flask(__name__)


@app.route('/')
def root(name=None):
    message = "Welcome, you are at the home page"
    return render_template('page.html', welcome=message)
    
    
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    ID = np.random.randint(100)
    return render_template('hello.html', name = name, ID = ID)

@app.route('/initdb')
def db_init():
    # make Database: inventory
    mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssword1"
    )
    cursor = mydb.cursor()
    
    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()
    
    #make Table: widegts 
    mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssword1",
    database="inventory"
    )
    cursor = mydb.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()
    
    return 'init database'

@app.route('/widgets')
def get_widgets() :
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssword1",
    database="inventory"
  )
  cursor = mydb.cursor()


  cursor.execute("SELECT * FROM widgets")

  row_headers=[x[0] for x in cursor.description] #this will extract row headers

  results = cursor.fetchall()
  json_data=[]
  for result in results:
    json_data.append(dict(zip(row_headers,result)))

  cursor.close()

  return json.dumps(json_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)