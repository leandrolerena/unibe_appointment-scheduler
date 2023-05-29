FROM python:3.11
LABEL authors="Leandro Lerena"

WORKDIR /app
RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy

COPY . .

CMD ["python3", "main.py"]