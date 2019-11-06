from models import engine, Post
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()