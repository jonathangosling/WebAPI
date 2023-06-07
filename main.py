from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from mangum import Mangum

app = FastAPI()   # create FastAPI instance
handler = Mangum(app) # handler for running on AWS Lambda
#app.mount("/html_files", StaticFiles(directory="/html_files"), name='html_files')

@app.get("/")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def root():          # will be run if a get request is made to the path "/" i.e. just the root in this case
    with open('/html_files/Front_Page.txt', 'r') as file:
        html_content = file.read().replace('\n','')
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/info")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def page():          # will be run if a get request is made to the path "/" i.e. just the root in this case
    with open('/html_files/Info_Page.txt', 'r') as file:
        html_content = file.read().replace('\n','')
    return HTMLResponse(content=html_content, status_code=200)
