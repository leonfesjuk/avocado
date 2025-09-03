from sqlalchemy import DateTime, create_engine, text, func, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from datetime import date, time, timedelta
import pandas as pd

from backend_python.resources.decorator import retry_on_operational_error, create_db_engine
from backend_python.config.settings import settings

Base = declarative_base()

class Controller(Base):
    __tablename__ = "controllers"
    __table_args__ = {'schema': 'avocado_sensor'}
    controller_id = Column(Integer, primary_key=True, autoincrement=True)

class Humidity(Base):
    __tablename__="humidity"
    __table_args__ = {'schema': 'avocado_sensor'}

    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("DEFAULT")) 
    controller_id = Column(Integer, ForeignKey('avocado_sensor.controllers.controller_id'))
    humidity = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())
    

@retry_on_operational_error()
def humidity_read(session):
    humidity = session.query(Humidity.id, Humidity.controller_id, Humidity.humidity, Humidity.timestamp).all()
    if not humidity:
        print("Empty humidity")
    result = pd.DataFrame(humidity)
    return result

@retry_on_operational_error()
def add_humidity_data(session, controller_id: int, humidity_value: int):
    try:
        new_humidity = Humidity(controller_id=controller_id, humidity=humidity_value)
        session.add(new_humidity)
        print(f"Added data to SQL server: Controller ID={controller_id}, Humidity={humidity_value}")
        return True
    except Exception as e:
        print(f"Error while preparing data to BD: {e}")
        return False

temp_engine = create_db_engine(settings.database_url)
Base.metadata.create_all(temp_engine)
temp_engine.dispose()





