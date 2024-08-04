FROM python:3.10-slim

COPY requirements.txt /app/requirements.txt
COPY yt-smuggler.py /app/yt-smuggler.py

RUN pip install -r /app/requirements.txt

RUN apt update && apt install -y ffmpeg

WORKDIR /app

CMD ["python", "yt-smuggler.py"]
