from decimal import Decimal
import os
from sqlite3.dbapi2 import Timestamp
from dotenv import load_dotenv
from sqlalchemy import DECIMAL, Column, DateTime, Integer, and_, create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field 

class ConnectionSettings(BaseSettings):
    """
    Class for downloading database connection configurations from .env
    """
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)

    DATABASE_URL: str = Field(..., alias="DATABASE_URL")


connections = ConnectionSettings()

if not connections.DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables or .env file.")
# Create the SQLAlchemy engine
engine = create_engine(connections.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()






class Avocado_Sensor(Base):
    __tablename__ = 'sensors'  
    __table_args__ = {'schema': 'avocado_sensor'}
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    humidity = Column(DECIMAL, nullable=False)
    temperature = Column(DECIMAL, nullable=False)
    light_brightness = Column(DECIMAL, nullable=False)

    
def get_avocado_sensors(id: int = None, time_start: DateTime = None, time_end: DateTime = None):
    db_session = SessionLocal()
    try:
        query = db_session.query(Avocado_Sensor)
        conditions = []
        if id is not None:
            conditions.append(Avocado_Sensor.id == id)
        
        if time_start is not None and time_end is not None:
            conditions.append(Avocado_Sensor.date_time.between(time_start, time_end))
        elif time_start is not None:
            conditions.append(Avocado_Sensor.date_time >= time_start)
        elif time_end is not None:
            conditions.append(Avocado_Sensor.date_time <= time_end)

        if conditions:
            avocado_sensors = query.filter(and_(*conditions)).all()
        else:
            
            return {"message": "No filters applied. Please provide at least one filter."}
        if not avocado_sensors:
            return {"message": "No data found for the specified filters."}
        
        data_for_df = []
        for s in avocado_sensors:
            data_for_df.append({
                "id": s.id,
                "date_time": s.date_time,
                "humidity": float(s.humidity), 
                "temperature": float(s.temperature),
                "light_brightness": float(s.light_brightness)
            })
        avocado_sensors_df = pd.DataFrame(data_for_df)
        return avocado_sensors_df
    except SQLAlchemyError as e:
        db_session.rollback()
        return {"error": str(e)}
    finally:
        db_session.close()
    

test = get_avocado_sensors(id=1)
print('Test DataFrame:')
print(test.head())
# This code is for testing purposes only. It will be removed in the final version.