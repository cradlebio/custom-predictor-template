FROM python:3.13-alpine3.22

WORKDIR /app
COPY custom_predictor.py /app

EXPOSE 8080/tcp
ENTRYPOINT ["python", "-c", "import custom_predictor; custom_predictor.run()"]
