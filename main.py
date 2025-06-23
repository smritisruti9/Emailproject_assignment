from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Signal
from process import process_signal

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SignalInput(BaseModel):
    sender: str
    subject: str
    timestamp: str
    links: list[HttpUrl]

@app.post("/ingest")
def ingest(signal: SignalInput, db: Session = Depends(get_db)):
    try:
        domain_status = process_signal(signal.sender)
        signal_entry = Signal(
            id=signal.timestamp,  
            sender=signal.sender,
            subject=signal.subject,
            links=", ".join([str(link) for link in signal.links]),
            domain=signal.sender.split('@')[-1],
            status=domain_status
        )
        db.add(signal_entry)
        db.commit()
        return {"message": "Signal stored", "status": domain_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
