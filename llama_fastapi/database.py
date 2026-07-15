from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "mysql+pymysql://root:root@localhost/chatdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# ✅ This line creates table automatically
Base.metadata.create_all(bind=engine)