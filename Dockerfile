FROM python:3.9-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY Pipfile /app
COPY Pipfile.lock /app

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app

EXPOSE 80
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
