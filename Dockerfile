FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","-c","from realtime_pipeline import WindowOperator; print('stream pipeline ready')"]
