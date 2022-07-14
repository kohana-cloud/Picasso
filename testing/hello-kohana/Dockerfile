FROM python:3.8.10

ADD src /src
WORKDIR /src

EXPOSE 8888

RUN pip3 install -r requirements.txt

CMD python3 app.py
