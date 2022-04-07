from datetime import datetime
from sqlalchemy import DateTime, create_engine
from sqlalchemy import Column,String,Integer,Float,ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# we will create our user tables

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    email = Column(String(50),unique=True)
    name = Column(String(50))
    password = Column(String(64))
    group = Column(Integer,default=1)
    created_at = Column(DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}| {self.name}|{self.group}"

class Review(Base):
    __tablename__ = 'reviews'
    reviewId = Column(String, primary_key=True)
    userName = Column(String)
    userImage = Column(String)
    content = Column(String)
    score = Column(Integer)
    thumbsUpCount = Column(Integer)
    reviewCreatedVersion = Column(String)
    at = Column(DateTime)
    replyContent = Column(String)
    repliedAt = Column(DateTime)
    app = Column(String)
    subjectivity = Column(Float)
    polarity = Column(Float)
    analysis = Column(String)

    def __str__(self):
        return f'{self.app} {self.score}'    

if __name__ == "__main__":
    engine = create_engine('sqlite:///db.sqlite3')
    Base.metadata.create_all(engine)


    

    

