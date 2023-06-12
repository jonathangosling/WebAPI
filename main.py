from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mangum import Mangum

# essentially, this is importing the html files to be returned as a response
# Note the "/" here is necessary when running on Lambda through Docker image!
templates = Jinja2Templates(directory="/html_files")

app = FastAPI()   # create FastAPI instance
handler = Mangum(app) # handler for running on AWS Lambda

@app.get("/", response_class=HTMLResponse)    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def root(request: Request):          # will be run if a get request is made to the path "/" i.e. just the root in this case
    return templates.TemplateResponse("Front_Page.html",
                                      {"request": request})

@app.get("/info", response_class=HTMLResponse)
async def page(request: Request):
    return templates.TemplateResponse("Info_Page.html",
                                      {"request": request})

# catch all other paths
@app.api_route("/{path_name:path}", methods=["GET"], response_class=HTMLResponse)
async def catch_all(request: Request):
    return templates.TemplateResponse("Catch_All_Page.html",
                                      {"request": request})