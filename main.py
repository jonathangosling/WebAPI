from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum

# essentially, this is importing the html files to be returned as a response
templates = Jinja2Templates(directory="/html_files_copy")

app = FastAPI()   # create FastAPI instance
handler = Mangum(app) # handler for running on AWS Lambda
#app.mount("/html_files", StaticFiles(directory="/html_files"), name='html_files')

@app.get("/", response_class=HTMLResponse)    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def root(request: Request):          # will be run if a get request is made to the path "/" i.e. just the root in this case
    # with open('./html_files/Front_Page.txt', 'r') as file:
    #     html_content = file.read().replace('\n','')
    #return HTMLResponse(content=html_content, status_code=200)
    return templates.TemplateResponse("Front_Page.html",
                                      {"request": request})

@app.get("/info", response_class=HTMLResponse)
async def page(request: Request):
    # with open('/html_files/Info_Page.txt', 'r') as file:
    #     html_content = file.read().replace('\n','')
    #return HTMLResponse(content=html_content, status_code=200)
    return templates.TemplateResponse("Info_Page.html",
                                      {"request": request})

# catch all other paths
@app.api_route("/{path_name:path}", methods=["GET"], response_class=HTMLResponse)
async def catch_all(request: Request, path_name: str):
    # with open('/html_files/Catch_All_Page.txt', 'r') as file:
    #     html_content = file.read().replace('\n','')
    #return HTMLResponse(content=html_content, status_code=200)
    return templates.TemplateResponse("Catch_All_Page.html",
                                      {"request": request})