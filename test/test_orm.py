# standard library
import os
from uuid import uuid4

# 3rd party modules
import pytest
from sqlalchemy import create_engine

# local modules
from core.db import models
from core.db.queries import QueriesApp

from test.config import DB_URI


class TestORM:
    # Connect using its own client
    db_client = QueriesApp(db_uri=DB_URI)

    # Calculate user_id
    this_run = str(uuid4())

    @pytest.fixture
    def root_user(self) -> models.User:
        return models.User(id=self.this_run)

    @pytest.fixture
    def first_question(self) -> models.Question:
        return models.Question(id=1, text="First question?")

    @pytest.fixture
    def second_question(self) -> models.Question:
        return models.Question(id=2, text="Second question?")

    @pytest.fixture
    def first_answer(self, root_user: models.User) -> models.Answer:
        return models.Answer(
            id=1,
            question_id=1, user_id=root_user.id, text="First answer for q1"
        )

    @pytest.fixture
    def second_answer(self, root_user: models.User) -> models.Answer:
        return models.Answer(
            id=2,
            question_id=1, user_id=root_user.id, text="Second answer for q1"
        )

    @pytest.fixture
    def fake_answer(self, root_user: models.User) -> models.Answer:
        return models.Answer(
            id=3,
            question_id=50, user_id=root_user.id, text="Answer for some fake Question"
        )

    def test_create_user(self, root_user: models.User):
        assert self.db_client.create_user(root_user), "Root user not created"

    def test_root_user_exists_by_id(self, root_user: models.User):
        assert root_user == self.db_client.get_user(root_user.id), "Root user not in DB (id)"

    def test_root_user_exists_by_all(self, root_user: models.User):
        assert root_user in self.db_client.get_all_users(), "Root user not in DB (user list)"

    def test_create_question(self, first_question: models.Question):
        assert self.db_client.create_question(first_question), "1st Question not created"

    def test_create_second_question(self, second_question: models.Question):
        assert self.db_client.create_question(second_question), "2nd question not created"

    def test_get_second_question(self, second_question: models.Question):
        assert self.db_client.get_question(second_question.id), "2nd question not got"

    def test_get_all_questions(self):
        assert len(self.db_client.get_all_questions()), "No questions found"

    def test_delete_unanswered_question(self, second_question: models.Question):
        assert self.db_client.delete_question(second_question.id), "Unanswered question not deleted"

    def test_create_answer(self, first_answer: models.Answer):
        assert self.db_client.create_answer(first_answer), "1st answer not created"

    def test_create_another_answer(self, second_answer: models.Answer):
        assert self.db_client.create_answer(second_answer), "2nd answer not created"

    def test_get_answers(self, first_question: models.Question):
        assert self.db_client.get_answers(first_question.id), "Answers for q1 not got"

    def test_delete_answered_question(self, first_question: models.Question):
        assert self.db_client.delete_question(first_question.id), "Answered question not deleted"

    def test_answer_nonexistent_question(self, fake_answer: models.Answer):
        assert not self.db_client.create_answer(fake_answer), "Fake answer WRONGFULLY created"

    def test_delete_root_user(self, root_user: models.User):
        assert self.db_client.delete_user(root_user.id), "Root user not deleted"
        self.db_client.close()
