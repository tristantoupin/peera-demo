FROM python:3

RUN pip install -r requirements.txt
RUN python app.py