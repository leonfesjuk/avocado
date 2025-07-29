from time import sleep
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from functools import wraps
from func_timeout import func_timeout, FunctionTimedOut
from dotenv import load_dotenv
import os
from backend_python.config.settings import settings
from sqlalchemy.exc import OperationalError

print("DEBUG: Decorator.py loaded and updated!")

load_dotenv()

mysql_server = settings.database_url

Base = declarative_base()

def create_db_engine(sql_server=mysql_server, max_retries=5, retry_delay=1, timeout=5):
    def connect_and_test():
        engine = create_engine(
            sql_server,
            #connect_args={'connect_timeout': timeout},
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=True
        )
        with engine.connect() as connection:
            pass
        return engine

    retries = 0
    last_exception = None
    while retries < max_retries:
        try:
            engine = func_timeout(timeout + 2, connect_and_test)
            return engine
        except FunctionTimedOut:
            retries += 1
            last_exception = OperationalError("Connection timed out repeatedly", [], {})
            print(f"DEBUG: Connection timed out in create_db_engine (attempt {retries}/{max_retries})")
        except OperationalError as e:
            retries += 1
            last_exception = e
            print(f"DEBUG: OperationalError in create_db_engine (attempt {retries}/{max_retries}): {e}")
        except Exception as e:
            retries += 1
            last_exception = e
            print(f"DEBUG: Unexpected error in create_db_engine (attempt {retries}/{max_retries}): {e}")

        if retries < max_retries:
            sleep(retry_delay)
    
    raise last_exception if last_exception else OperationalError("Failed to connect after multiple retries with unknown error.")


def retry_on_operational_error(sql_server=mysql_server, max_retries=5, retry_delay=3, timeout=10, raise_on_failure=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            last_exception = None
            
            while retries < max_retries:
                engine = None
                session = None
                try:
                    engine = create_db_engine(
                        sql_server=sql_server,
                        max_retries=max_retries,
                        retry_delay=retry_delay,
                        timeout=timeout
                    )
                    
                    Session = sessionmaker(
                        bind=engine,
                        expire_on_commit=False,
                        autoflush=False
                    )
                    session = Session()
                    
                    #try:
                       #session.execute(text(f"SET SESSION wait_timeout = {timeout}"))
                    #except Exception:
                        #pass
                    
                    result = func(session, *args, **kwargs)
                    
                    session.commit()
                    return result
                    
                except (OperationalError, FunctionTimedOut) as e:
                    retries += 1
                    last_exception = e
                    print(f"DEBUG: OperationalError/Timeout in transaction (attempt {retries}/{max_retries}): {e}")
                    
                    if session:
                        session.rollback()
                        
                    if retries < max_retries:
                        sleep(retry_delay)
                    
                except Exception as e:
                    retries += 1
                    last_exception = e
                    print(f"DEBUG: Other error in transaction (attempt {retries}/{max_retries}): {e}")
                    
                    if session:
                        session.rollback()
                        
                    if retries < max_retries:
                        sleep(retry_delay)
                finally:
                    if session is not None:
                        try:
                            session.close()
                        except Exception:
                            pass
                    if engine is not None:
                        try:
                            engine.dispose()
                        except Exception:
                            pass
            
            if raise_on_failure and last_exception:
                raise last_exception
            return None

        return wrapper
    return decorator