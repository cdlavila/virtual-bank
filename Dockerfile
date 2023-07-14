FROM python:3.10

WORKDIR /code

COPY . /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uwsgi", "--http", ":8000", "--module", "django_app.wsgi"]

# Commands
# docker build -t virtual-bank .
# docker run -d --name virtual-bank -p 80:80 virtual-bank
# remember the env variables