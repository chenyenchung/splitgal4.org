FROM python:3
RUN pip3 install --upgrade pip
RUN pip3 install django openpyxl six
COPY . /home/splitgal4_org
WORKDIR /home/splitgal4_org
RUN python manage.py collectstatic
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
