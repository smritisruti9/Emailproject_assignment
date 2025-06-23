from sqlalchemy import Column, String, Text
from database import Base

class Signal(Base):
    __tablename__ = "signals"
    id = Column(String, primary_key=True, index=True)  # Add primary key
    sender = Column(String)
    subject = Column(String)
    links = Column(Text)
    domain = Column(String, default="")
    status = Column(String, default="new")  



