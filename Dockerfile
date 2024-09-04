FROM python:3.12

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . src

# EXPOSE 8000 

# ENTRYPOINT -

# CMD python manage.py runserver