# default library modules
from datetime import datetime
from numbers import Number

# 3rd party modules
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Annotated, Optional


class User(BaseModel):
    id: Annotated[str, Field(min_length=1, max_length=36)]

    # ORM-related, also strip whitespace from left and right
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class Question(BaseModel):
    # model fields
    id: int
    text: Annotated[
        str, Field(min_length=2)]  # at least two characters — 1 alphanumeric symbol + 1 question mark
    created_at: Optional[datetime] = None

    # ORM related, also strip whitespace from left and right
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    # field validators
    @field_validator("text", mode="before")
    @classmethod
    def validate_text(cls, value):
        if isinstance(value, str):
            return value

        else:
            raise ValueError("Only strings are supported as questions.")


class Answer(BaseModel):
    # model fields
    id: int
    question_id: Optional[int] = None
    user_id: str
    text: Annotated[str, Field(min_length=1)]  # at least one alphanumeric character (see `validate_text`)
    created_at: Optional[datetime] = None

    # ORM-related, also strip whitespace from left and right
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    # field validators
    @field_validator("text", mode="before")
    @classmethod
    def validate_text(cls, value):
        if isinstance(value, Number):
            return str(value)

        elif isinstance(value, str):
            return value

        else:
            raise ValueError("Only strings and "
                             "numbers are supported as answers.")
