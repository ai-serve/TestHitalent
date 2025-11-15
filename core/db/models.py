# python default library modules
import datetime

# 3rd party modules
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    # columns -----------------------------------
    id = Column(String, primary_key=True)

    # comparison of objects
    def __eq__(self, other):
        return self.id == other.id


class Question(Base):
    __tablename__ = "Question"

    # columns -----------------------------------
    id = Column(Integer, primary_key=True)
    text = Column(String)

    # timezone unaware db object to ensure compatibility with many RDBMS and consistency
    created_at = Column(
        DateTime(timezone=False),
        default=lambda: datetime.datetime.now(datetime.UTC)
    )
    # -------------------------------------------


class Answer(Base):
    __tablename__ = "Answer"

    # columns -----------------------------------
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("Question.id", ondelete="CASCADE"))
    user_id = Column(String, ForeignKey("User.id", ondelete="CASCADE"))
    text = Column(String)

    # timezone unaware db object to ensure compatibility with many RDBMS and consistency
    created_at = Column(
        DateTime(timezone=False),
        default=lambda: datetime.datetime.now(datetime.UTC)
    )
    # -------------------------------------------
