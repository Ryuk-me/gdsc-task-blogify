FROM python:3.11.0
ENV ENV=prod
ENV TZ=Asia/Kolkata
COPY ./app/requirements.txt requirements.txt
COPY . .
RUN pip3 install -r requirements.txt