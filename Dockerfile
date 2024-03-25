FROM python:3.10.13-alpine

COPY . /data
WORKDIR /data

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m", "main.py" ]