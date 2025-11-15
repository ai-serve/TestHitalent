# standard library modules
from uuid import uuid4

# 3rd party modules
import pytest
import requests

# local modules
from core.validation_models import datamodels
from test.config import API_BASE_URL


class TestAPI:
    this_run = str(uuid4())

    @pytest.fixture
    def root_user(self) -> datamodels.User:
        return datamodels.User(id=self.this_run)

    @pytest.fixture
    def first_question(self) -> datamodels.Question:
        return datamodels.Question(id=1, text="First question?")

    @pytest.fixture
    def second_question(self) -> datamodels.Question:
        return datamodels.Question(id=2, text="Second question?")

    @pytest.fixture
    def first_answer(self, root_user: datamodels.User) -> datamodels.Answer:
        return datamodels.Answer(
            id=1,
            question_id=1, user_id=root_user.id, text="First answer for q1"
        )

    @pytest.fixture
    def second_answer(self, root_user: datamodels.User) -> datamodels.Answer:
        return datamodels.Answer(
            id=2,
            question_id=1, user_id=root_user.id, text="Second answer for q1"
        )

    @pytest.fixture
    def fake_answer(self, root_user: datamodels.User) -> datamodels.Answer:
        return datamodels.Answer(
            id=3,
            question_id=50, user_id=root_user.id, text="Answer for some fake Question"
        )

    def test_home(self):
        assert requests.get(
            API_BASE_URL + "/"
        ).status_code == 200, "API not functioning properly"

    def test_create_user(self, root_user: datamodels.User):
        assert requests.post(
            API_BASE_URL + "/new_user",
            json=root_user.model_dump()
        ).status_code == 201, "Root user not created"

    def test_create_question(self, first_question: datamodels.Question):
        assert requests.post(
            API_BASE_URL + "/questions",
            json=first_question.model_dump()
        ).status_code == 201, "1st Question not created"

    def test_create_second_question(self, second_question: datamodels.Question):
        assert requests.post(
            API_BASE_URL + "/questions",
            json=second_question.model_dump()
        ).status_code == 201, "2nd question not created"

    def test_get_second_question(self, second_question: datamodels.Question):
        q, ans_lst = requests.get(
            API_BASE_URL + f"/questions/{second_question.id}",
        ).json()
        assert second_question.id == q.get("id"), "2nd question not got"

    def test_get_all_questions(self):
        resp = requests.get(API_BASE_URL + "/questions")
        assert len(resp.json()), "No questions found"

    def test_delete_unanswered_question(self, second_question: datamodels.Question):
        assert requests.delete(
            API_BASE_URL + f"/questions/{second_question.id}",
        ).status_code == 200, "Unanswered question not deleted"

    def test_create_answer(self, first_answer: datamodels.Answer):
        ans = first_answer.model_dump(exclude={"question_id"})
        qid = first_answer.question_id
        assert requests.post(
            API_BASE_URL + f"/questions/{qid}/answers",
            json=ans
        ).status_code == 201, "1st answer not created"

    def test_create_another_answer(self, second_answer: datamodels.Answer):
        ans = second_answer.model_dump(exclude={"question_id"})
        qid = second_answer.question_id
        assert requests.post(
            API_BASE_URL + f"/questions/{qid}/answers",
            json=ans
        ).status_code == 201, "2nd answer not created"

    def test_get_answer_by_id(self, first_answer: datamodels.Question):
        assert requests.get(
            API_BASE_URL + f"/answers/{first_answer.id}",
        ).status_code == 200, "Answers for q1 not got"

    def test_delete_answer_by_id(self, second_answer: datamodels.Question):
        assert requests.delete(
            API_BASE_URL + f"/answers/{second_answer.id}",
        ).status_code == 200, "Answers for q1 not deleted"

    def test_delete_answered_question(self, first_question: datamodels.Question):
        assert requests.delete(
            API_BASE_URL + f"/questions/{first_question.id}",
        ).status_code == 200, "Answered question not deleted"

    def test_answer_nonexistent_question(self, fake_answer: datamodels.Answer):
        ans = fake_answer.model_dump(exclude={"question_id"})
        qid = fake_answer.question_id
        resp = requests.post(
            API_BASE_URL + f"/questions/{qid}/answers",
            json=ans
        )
        assert resp.status_code == 500, "Fake answer WRONGFULLY created"

    def test_delete_root_user(self, root_user: datamodels.User):
        assert requests.delete(API_BASE_URL + f"/delete_user/{root_user.id}"), "Root user not deleted"
