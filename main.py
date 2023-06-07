from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from mangum import Mangum

app = FastAPI()   # create FastAPI instance
handler = Mangum(app) # handler for running on AWS Lambda
#app.mount("/imgs", StaticFiles(directory="/imgs"), name='images')

@app.get("/")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def root():          # will be run if a get request is made to the path "/" i.e. just the root in this case
    file = open('./Front_Page.txt', 'r')
    html_content = file.read().replace('\n','')
    file.close()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/info")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def page():          # will be run if a get request is made to the path "/" i.e. just the root in this case
    html_content = """
    <html>
    <body>
        <h1>What's this all about?</h1>
        <p>I created this page after learning a bit about FastAPI in python.
        <br>I wanted to have a go at using FastAPI to create a simple webapp which would be hosted on serverless AWS.
        <br>Using this project, I have been able to practise a few things:
            <ul>
                <li>FastAPI</li>
                <li>AWS Lambda serverless hosting</li>
                <li>AWS Route 53 DNS</li>
                <li>AWS API Gateway (to set up a connection between Route 53 and lambda)</li>
                <li>Building and deploying Docker images</li>
                <li>Setting up CI/CD pipelines using AWS CodeBuild</li>
                <li>Some basic html (I'm still in the process of that, as I'm sure you can tell)</li>
            </ul>
            Here's a schematic of the pipeline:
            <br>
            <img src="https://my-webpage-images.s3.amazonaws.com/webapp_pipeline.png" width="1300">
        </p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
