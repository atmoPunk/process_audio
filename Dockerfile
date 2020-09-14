FROM ubuntu:16.04

WORKDIR /code

COPY requirements.txt .

RUN apt update

RUN apt install -y ffmpeg python3-pip

RUN pip3 install -r requirements.txt

COPY src/ .

ENTRYPOINT ["./process_audio.py"]
