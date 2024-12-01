from fastapi import FastAPI
from subscription.router import router as router_subscription

app = FastAPI()

@app.get("/")
def home_page():
    return {"message" : "Hi there! I'm using What's App"}

app.include_router(router_subscription)