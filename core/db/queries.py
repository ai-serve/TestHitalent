# standard library modules
import sys
from typing import List, cast

# 3rd party modules
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import InstrumentedAttribute, sessionmaker, close_all_sessions

# local modules
from core.db.models import User, Question, Answer, Base


class QueriesApp:
    def __init__(self, engine=None, db_uri=None):
        if engine:
            self.engine = engine
        else:

            if db_uri is None:
                sys.exit(1)
            self.engine = create_engine(db_uri)

        self.session = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)

    @staticmethod
    def convert_model_to_orm(model_obj: BaseModel, model_orm: type[Base]):
        return model_orm(**model_obj.model_dump())

    def close(self):
        close_all_sessions()
        self.engine.dispose()


    # QUERIES
    # Users -----------------------------------------
    def get_user(self, user_id: str | InstrumentedAttribute[str]) -> User | None:
        try:
            with self.session.begin() as session:
                user = session.get(User, user_id)
                return user
        except Exception as e:
            print(f"[ERROR]\t{e}")
            return None


    def get_all_users(self) -> List[User] | None:
        try:
            with self.session.begin() as session:
                users: List[User] = cast(
                    List[User],
                    session.execute(select(User)).scalars().all()
                )
                return users

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return None


    def create_user(self, user: User) -> bool:
        try:
            with self.session.begin() as session:
                session.add(user)
                session.commit()
                return True

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return False


    def delete_user(self, user_id: str | InstrumentedAttribute[str]) -> bool:
        try:
            with self.session.begin() as session:
                user = session.get(User, user_id)
                session.delete(user)
                session.commit()
                return True

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return False


    # Questions -------------------------------------
    def get_question(self, question_id: int | InstrumentedAttribute[int]) -> Question | None:
        try:
            with self.session.begin() as session:
                q = session.get(Question, question_id)
                return q

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return None


    def get_all_questions(self) -> List[Question] | None:
        try:
            with self.session.begin() as session:
                q: List[Question] = cast(
                    List[Question],
                    session.execute(
                        select(Question)
                    ).scalars().all()
                )
                return q

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return None


    def create_question(self, question: Question) -> bool:
        try:
            with self.session.begin() as session:
                session.add(question)
                session.commit()
                return True

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return False


    def delete_question(self, question_id: int | InstrumentedAttribute[int]) -> bool:
        try:
            with self.session.begin() as session:
                question = session.get(Question, question_id)
                session.delete(question)
                session.commit()
                return True

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return False


    # Answers ---------------------------------------
    def get_answers(self, question_id: int | InstrumentedAttribute[int]) -> List[Answer] | None:
        try:
            with self.session.begin() as session:
                answers: List[Answer] = cast(
                    List[Answer],
                    session.execute(
                        select(Answer).where(Answer.question_id == question_id)
                    ).scalars().all()
                )
                return answers

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return None


    def get_answer(self, answer_id: int | InstrumentedAttribute[int]) -> Answer | None:
        try:
            with self.session.begin() as session:
                answer = session.get(Answer, answer_id)
                return answer

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return None


    def create_answer(self, answer: Answer) -> bool:
        try:
            question_id: int | InstrumentedAttribute[int] = answer.question_id
            is_question_in_db: bool = self.get_question(question_id)
            if is_question_in_db:

                with self.session.begin() as session:
                    session.add(answer)
                    session.commit()
                    return True
            else:
                return False

        except Exception as e:
            print(f"[ERROR]\tGeneral exception: {e}")
            return False


    def delete_answer(self, answer_id: int | InstrumentedAttribute[int]) -> bool:
        try:
            with self.session.begin() as session:
                answer = session.get(Answer, answer_id)
                session.delete(answer)
                session.commit()
                return True

        except Exception as e:
            print(f"[ERROR]\t{e}")
            return False
