import uvicorn
from fastapi import Depends, FastAPI
from .database import Session, get_session

app = FastAPI()

@app.get("/")
def index(db: Session = Depends(get_session)):
    return "Hello world!"

if __name__ == "__main__":
    uvicorn.run(app=app)