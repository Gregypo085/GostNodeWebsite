from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

api = FastAPI()

api.mount("/static", StaticFiles(directory="static"), name="static") # Mount static files directory

templates = Jinja2Templates(directory="templates") # Set up templates directory

@api.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) # Render index.html template

# def index():
#     return {"message": "Hello, Worlds and Greg! VSCode test 3"}

#run fastapi dev main.py