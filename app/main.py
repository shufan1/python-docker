from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import mysql.connector
import json

#from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates/")
#app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {"page" :"main page"}
    return templates.TemplateResponse("page.html",{"request":request,"data":data})

@app.get("/number", response_class=HTMLResponse)
async def page(request: Request):
    data = {
        "page": np.random.randint(100)
    }
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

@app.route('/initdb')
async def db_init():
    mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssword1"
    )
    cursor = mydb.cursor()
    
    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()
    
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

    
@app.get('/widgets')
async def get_widgets() :
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@sswosrd1",
    database="mysql"
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
    uvicorn.run(app, port=8080, host='0.0.0.0')