from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mangum import Mangum

app = FastAPI()   # create FastAPI instance
handler = Mangum(app) # handler for running on AWS Lambda

@app.get("/")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def root():          # will be run if a get request is made to the path "/" i.e. just the root in this case
    html_content = """
    <html>
    <body>
        <h1>Welcome...</h1>
        <p>Site under development, please come back later :) </p>
        <p>Click <a href="/page">here</a> to test my redirection.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/page")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def page():          # will be run if a get request is made to the path "/" i.e. just the root in this case
    return 'Oops you found me'
