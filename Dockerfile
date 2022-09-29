FROM python:3.8-slim-bullseye

COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

VOLUME /input
VOLUME /output

WORKDIR /

CMD ["python", "main.py"]

## build:
# sudo docker build -t task_etl:latest .
## run:
# sudo docker run -v $(pwd)/input:/input -v $(pwd)/output:/output -it task_etl:latest
