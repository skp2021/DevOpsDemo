FROM python:3.7-slim

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

CMD [ "python3","app.py" ]
