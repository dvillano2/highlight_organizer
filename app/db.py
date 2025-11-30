import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

LOCAL_URL = os.environ.get("LOCL_DB_URL")
local_engine = create_engine(LOCAL_URL, echo=True, future=True)
LocalSession = sessionmaker(
    bind=local_engine, autoflush=False, autocommit=False
)
