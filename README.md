### commands:
```
build:
sudo docker build -t task_etl:latest .

run:
sudo docker run -v $(pwd)/input:/input -v $(pwd)/output:/output -it task_etl:latest
```
