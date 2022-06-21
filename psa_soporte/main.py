import uvicorn
from fastapi import Depends, FastAPI
from .database import Session, engine, get_session
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def index(db: Session = Depends(get_session)):
    return "Hello world!"

if __name__ == "__main__":
    uvicorn.run(app=app)