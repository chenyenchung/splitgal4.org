FROM python:3
RUN pip3 install --upgrade pip
RUN pip3 install django openpyxl six gunicorn requests django-turnstile
COPY . /home/splitgal4_org
WORKDIR /home/splitgal4_org
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "--bind" , "0.0.0.0:8000", "splitgal4db.wsgi"]
