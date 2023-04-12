from fastapi import FastAPI

app = FastAPI()   # create FastAPI instance
@app.get("/")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def root():          # will be run if a get request is made to the path "/" i.e. just the root in this case
    return 'Site under development, please come back later :)'

