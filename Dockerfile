FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install virtualenv

RUN virtualenv  env
RUN env\Scripts\activate

#COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#COPY . .

# running migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

RUN python manage.py runserver

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
