from sqlalchemy import create_engine
from .models import Base
SQL_URL = "sqlite:///tg_bot.db"

engine = create_engine(SQL_URL,echo=True)

Base.metadata.create_all(bind=engine)
