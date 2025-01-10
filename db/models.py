from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String
from database import Base

class Temperatures(Base):
    __tablename__ = 'temperatures'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    house_temperature = Column(Float)
    outside_temperature = Column(Float)
    
    
class Weather(Base):
    __tablename__ = 'weather'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now) 
    weather = Column(String)
    