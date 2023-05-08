FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /testPythonVK
COPY . /testPythonVK
RUN pip3 install -r requirements.txt
RUN python3 manage.py runserver
COPY . .