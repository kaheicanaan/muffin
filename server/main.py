from fastapi import FastAPI

from routers import chatrooms, login, users

app = FastAPI()

app.include_router(chatrooms.router, prefix="/chatrooms", tags=["chatrooms"])
app.include_router(login.router, prefix="/login", tags=["login"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/", status_code=200)
def root():
    return {"message": "Hello world from muffin."}
