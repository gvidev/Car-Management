from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = "sqlite:///./car-management.db"
engine = create_engine(database_url, echo=True)
Session = sessionmaker(engine)