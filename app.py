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

@app.route('/initcitydb')
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
    cursor.execute("DROP TABLE IF EXISTS cities")
    cursor.execute("CREATE TABLE cities (name VARCHAR(255), long_and_lat VARCHAR(255));")
    cursor.execute("INSERT INTO cities (name,long_and_lat) VALUES ('San Francisco', '(-194.0, 53.0)');")
    print("here2")
    cursor.execute("INSERT INTO cities (name,long_and_lat) VALUES ('Springfield',	'(39.8,	-89.7)');")
    
    cursor.execute("SELECT * FROM cities;")
    
    row_headers=[x[0] for x in cursor.description]  
    results = cursor.fetchall()
    json_data=[]
    for result in results:
      json_data.append(dict(zip(row_headers,result)))
    
    cursor.close()
    
    return json.dumps(json_data)
      

@app.route('/cities')
def get_cities() :
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssword1",
    database="location"
  )
  cursor = mydb.cursor()
  cursor.execute("SELECT * FROM cities;")
  

  row_headers=[x[0] for x in cursor.description] #this will extract row headers
  
  results = cursor.fetchall()
  json_data=[]
  for result in results:
    json_data.append(dict(zip(row_headers,result)))
  
  cursor.close()
  
  return json.dumps(json_data)

@app.route('/addcity/<city>/<long>/<lat>')
def add_city(city=None, long=None,lat=None):
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssword1",
    database="location"
  )
  
  long_and_lat ="("+str(long)+","+ str(lat)+")"
  
  cursor = mydb.cursor()
  cursor.execute("INSERT INTO cities (name,long_and_lat) VALUES ('{0}', '{1}');".format(city,long_and_lat))
  cursor.close()
  return '{"new entry":[{"city":{0},"long_lat":{1}}]}'.format(city,long_and_lat)
    
  
  
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
