from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.routers import blog, user, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)

@app.get("/")
def index():
    return {"welcome": "FastAPI"}

# if __name__ == "__main__":
#     uvicorn.run("blog.main:app", port=8000, reload=True)