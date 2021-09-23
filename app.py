from flask import Flask
from flask import render_template
import mysql.connector
import json
import numpy as np

app = Flask(__name__)

@app.route('/')
def root():
    message = "Welcome, you are at the home page"
    return render_template('page.html', welcome=message)
    
    
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    ID = np.random.randint(100)
    return render_template('hello.html', name = name, ID = ID)

@app.route('/initcitybikedb')
def db_init():
    # make Database: location
    mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssword1"
    )
    cursor = mydb.cursor()
    print("here")
    cursor.execute("DROP DATABASE IF EXISTS location")
    cursor.execute("CREATE DATABASE location")
    cursor.close()
    
    #make Table: cities 
    mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssword1",
    database="location"
    )
    cursor = mydb.cursor()
    cursor.execute("DROP TABLE IF EXISTS citybike")
    cursor.execute("CREATE TABLE citybike (name VARCHAR(255), bicycle_friendly VARCHAR(255));")
    cursor.execute("INSERT INTO citybike (name,bicycle_friendly) VALUES ('San Francisco', 'No');")
    cursor.execute("INSERT INTO citybike (name,bicycle_friendly) VALUES ('Springfield',	'No');")
    mydb.commit()
    cursor.close()
    
    return "initdb"
        

@app.route('/citybike')
def get_citybike() :
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssword1",
        database="location"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM citybike;")
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    cursor.close()
    
    return json.dumps(json_data)

@app.route('/addcity/<city>/<bicycle_friendly>')
def add_city(city=None, bicycle_friendly=None):
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssword1",
        database="location"
    )
    
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO citybike (name,bicycle_friendly) VALUES ('{0}', '{1}');".format(city,bicycle_friendly))
    mydb.commit()
    return "%s added"%city
    
        
    
    
@app.route('/timezones')
def get_timezones() :
    mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssword1",
    database="mysql"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM time_zone_name LIMIT 10;")

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    cursor.close()

    return json.dumps(json_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
