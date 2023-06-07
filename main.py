from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRouter
from mangum import Mangum

app = FastAPI()   # create FastAPI instance
router = APIRouter()
handler = Mangum(app) # handler for running on AWS Lambda
#app.mount("/html_files", StaticFiles(directory="/html_files"), name='html_files')

@router.get("/")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
async def root():          # will be run if a get request is made to the path "/" i.e. just the root in this case
    with open('/html_files/Front_Page.txt', 'r') as file:
        html_content = file.read().replace('\n','')
    return HTMLResponse(content=html_content, status_code=200)

# @app.get("/info")    # define path operation decorator. Tells the FastAPI that function right below is responsible for handling requests that go to the path "/" using a get operation
# async def page():          # will be run if a get request is made to the path "/" i.e. just the root in this case
#     with open('/html_files/Info_Page.txt', 'r') as file:
#         html_content = file.read().replace('\n','')
#     return HTMLResponse(content=html_content, status_code=200)

@router.middleware("http")
async def handle_undefined_endpoints(request: Request, call_next):
    response = await call_next(request)
    
    # Check if the endpoint is not explicitly defined
    if response.status_code == 404 and isinstance(request.scope["endpoint"], Match):
        # Add a link back to the root in the response content
        root_link = f'<a href="/">Back to Root</a>'
        response.content = response.content.replace(b'</body>', f'{root_link}</body>'.encode())
    
    return response

app.include_router(router)