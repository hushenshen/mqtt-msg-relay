FROM python:slim
WORKDIR /app
COPY main.py .
RUN pip3 install paho-mqtt
CMD ["python", "main.py"]
