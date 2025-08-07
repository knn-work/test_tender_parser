from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core import app_config

Base = declarative_base()

engine = create_engine(
    app_config.database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
