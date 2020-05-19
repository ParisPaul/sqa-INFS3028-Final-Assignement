FROM python:3.7.7-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

VOLUME ["/code"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]