# standard library modules
import os
import sys
from contextlib import asynccontextmanager

# 3rd party modules
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# local modules
from core.db import models
from core.db.queries import QueriesApp
from core.validation_models import datamodels as datamodels


db_client: QueriesApp | None = None

@asynccontextmanager
async def start_and_stop_engine(rout: APIRouter = None):
    global db_client
    db_uri = os.getenv("DB_URI")
    if db_uri is None:
        sys.exit("[ERROR]\tDB_URI not set.")
    db_client = QueriesApp(db_uri=db_uri)

    yield

    db_client.close()


router = APIRouter(
    lifespan=start_and_stop_engine
)


@router.get(path="/", tags=["home"])
async def home() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"ok": True, "status_code": 200})


@router.post(path="/new_user", tags=["users"])
async def create_user(user: datamodels.User) -> JSONResponse:

    try:
        user_orm = db_client.convert_model_to_orm(user, models.User)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"detail":f"[ERROR]\t{e}"})

    try:
        db_response: bool = db_client.create_user(user_orm)
        if not db_response:
            raise Exception("Unexpected DB response")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"detail": f"[ERROR]\t{e}"})

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"ok": True, "status_code": 201})


@router.delete(path="/delete_user/{user_id}", tags=["users"])
async def delete_user_by_id(user_id: str) -> JSONResponse:

    try:
        db_response: bool = db_client.delete_user(user_id)
        if not db_response:
            raise Exception("Unexpected DB response")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"detail": f"[ERROR]\t{e}"})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"ok": True, "status_code": 200})


# Questions ------------
@router.get(path="/questions", tags=["questions"])
async def get_all_questions() -> list[datamodels.Question]:
    """"""

    qs: list[models.Question] | None = db_client.get_all_questions()
    if qs:
        for i in range(len(qs)):
            try:
                qs[i]: datamodels.Question = datamodels.Question.model_validate(qs[i])
            except ValidationError as ve:
                print(f"[ERROR]\t{ve}")

        return qs
    else:
        return []


@router.post(path="/questions", tags=["questions"])
async def post_one_question(question: datamodels.Question) -> JSONResponse:
    """"""

    try:
        question_orm = db_client.convert_model_to_orm(question, models.Question)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"detail":f"[ERROR]\t{e}"})

    try:
        db_response: bool = db_client.create_question(question_orm)
        if not db_response:
            raise Exception("Unexpected DB response")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"detail": f"[ERROR]\t{e}"})

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"ok": True, "status_code": 201})


@router.get(path="/questions/{question_id}", tags=["questions"])
async def get_question_and_all_answers_by_id(
        question_id: int
) -> tuple[datamodels.Question | None, list[datamodels.Answer] | None]:
    """"""
    question: models.Question | None = db_client.get_question(question_id)

    if question:
        answers: list[models.Answer | None] = db_client.get_answers(question_id)
        for i in range(len(answers)):
            try:
                answers[i] = datamodels.Answer.model_validate(
                    answers[i]).model_dump()
            except ValidationError as ve:
                print(f"[ERROR]\t{ve}")

        return question, answers

    return None, None


@router.delete(path="/questions/{question_id}", tags=["questions"])
async def delete_question_and_all_answers_by_id(
        question_id: int
) -> JSONResponse:
    """"""

    try:
        # on delete cascade is EXPECTED on DB Backend
        db_response: bool = db_client.delete_question(question_id)
        if not db_response:
            raise Exception("Unexpected DB response")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"detail": f"[ERROR]\t{e}"})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"ok": True, "status_code": 200})
# ----------------------

# Answers --------------

@router.post(path="/questions/{question_id}/answers", tags=["answers"])
async def post_answer_by_question_id(
        question_id: int,
        answer: datamodels.Answer
) -> JSONResponse:
    """"""

    try:
        _answer = datamodels.Answer.model_validate(
            answer.model_dump() | {"question_id": question_id})
        answer_orm = db_client.convert_model_to_orm(_answer, models.Answer)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"detail":f"[ERROR]\t{e}"})

    try:
        db_response: bool = db_client.create_answer(answer_orm)
        if not db_response:
            raise Exception("Unexpected DB response")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"detail": f"[ERROR]\t{e}"})

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"ok": True, "status_code": 201})


@router.get(path="/answers/{answer_id}", tags=["answers"])
async def get_answer_by_id(answer_id: int):
    """"""

    try:
        db_response = db_client.get_answer(answer_id)
        if not db_response:
            raise Exception("Unexpected DB response")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"detail":f"[ERROR]\t{e}"})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"ok": True, "status_code": 200})


@router.delete(path="/answers/{answer_id}", tags=["answers"])
async def delete_answer_by_id(
        answer_id: int
) -> JSONResponse:
    """"""

    try:
        db_response = db_client.delete_answer(answer_id)
        if not db_response:
            raise Exception("Unexpected DB response")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"detail": f"[ERROR]\t{e}"})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"ok": True, "status_code": 200})
# ----------------------
