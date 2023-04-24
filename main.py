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
        <h1>Welcome To My Page</h1>
        <p>You may be wondering why this, rather blank (for now) webpage, exists.</p>
        <p>Well, click <a href="/page">here</a> to find out a little more.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/info")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def page():          # will be run if a get request is made to the path "/" i.e. just the root in this case
    html_content = """
    <html>
    <body>
        <h1>What's this all about?</h1>
        <p>I created this page after learning a bit about FastAPI in python.
        <br>I wanted to try using FastAPI to create a simple webapp which would be live, hosted on serverless AWS.
        <br>I have used this webapp to practise a few things:
        <ul>
            <li>FastAPI</li>
            <li>AWS Lambda serverless hosting</li>
            <li>AWS Route 53 DNS</li>
            <li>AWS API Gateway (to set up a connection between Route 53 and lambda)</li>
            <li>Building and deploying Docker images</li>
            <li>Setting up CI/CD pipelines using AWS CodeBuild</li>
            </ul>
        </p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
