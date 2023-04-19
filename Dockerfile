FROM python:3.8.10-slim-buster

RUN apt update && apt upgrade -y
WORKDIR /src
COPY  . /src/

RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN python3 preprocess.py
CMD [ "sh", "entrypoint.sh" ]