from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from psycopg.rows import dict_row
import time
from .config import settings


# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<IP-address/hostname>:<port>/<database_name>"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# establish the connection to DB
# while True:
#     try:
#         # conn = psycopg.connect(host,database,user,password)

#         conn = psycopg.connect(
#             host="localhost",
#             dbname="fastapi",
#             user="postgres",
#             password="Hajar",
#             row_factory=dict_row,  # this is used to get the column name
#         )

#         cursor = conn.cursor()

#         print("Database connection was successfull!")

#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("tError:", error)
#         time.sleep(2)
