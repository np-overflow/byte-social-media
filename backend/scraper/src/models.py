from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///site.db', echo=True)
Base = declarative_base()

class Post(Base):
    __tablename__ = 'post'

    post_id = Column(Integer, primary_key=True)
    name    = Column(String)
    date    = Column(DateTime)
    message = Column(String)
    caption = Column(String)
    photo   = Column(String) # Fixed Length should be 32 + 4 (4 for extension)

    def __init__(self, name, date, message, photo, caption):
        self.name       = name
        self.date       = date
        self.message    = message
        self.photo      = photo
        self.caption    = caption

Base.metadata.create_all(engine)