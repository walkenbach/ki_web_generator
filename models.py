from sqlalchemy import Column, Integer, String, Text
from database import Base

class RequestLog(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text)
    output_text = Column(Text)






