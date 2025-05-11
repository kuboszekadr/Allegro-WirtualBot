FROM python:3.12-bullseye

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.in-project true