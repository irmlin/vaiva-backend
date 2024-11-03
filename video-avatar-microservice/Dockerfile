FROM paidax/dev-containers:cuda11.6-py3.8

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && \
    apt install -y \
    ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu113

COPY main.py ./
COPY src/ src/