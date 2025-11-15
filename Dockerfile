FROM python:3.13.6-slim
LABEL authors="stan"

RUN mkdir core
RUN mkdir core/main
RUN mkdir core/db
RUN mkdir core/validation_models

COPY core/requirements.txt ./core
COPY core/__init__.py ./core
COPY core/main ./core/main/
COPY core/db ./core/db/
COPY core/validation_models ./core/validation_models/


RUN pip install --root-user-action=ignore --upgrade pip && pip install --root-user-action=ignore -r /core/requirements.txt && rm -rf ~/.cache/pip
