import uvicorn
from fastapi import Depends, FastAPI
from database import Base, engine, Session, get_session
from psa_soporte.models import Employee, Ticket

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def index(db: Session = Depends(get_session)):
    return "Hello world!"

if __name__ == "__main__":
    uvicorn.run(app=app)