from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np

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

    
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')