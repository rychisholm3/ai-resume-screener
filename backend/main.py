# import FastAPI so we can create a web server
from fastapi import FastAPI

# create the app instance (this is our backend server)
app = FastAPI()

# define a route for the homepage ("/")
# when someone visits the root URL, this function runs
@app.get("/")
def home():
    # return a simple message to show the server is working
    return {"message": "AI Resume Screener is running"}