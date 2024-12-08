FROM nvidia/cuda:11.6.2-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && \
    apt install -y \
    python3.9 \
    python3.9-distutils \
    python3.9-dev \
    python3.9-venv \
    curl \
    git \
    ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.9 get-pip.py && \
    rm get-pip.py

RUN which pip3.9

# Set Python 3.9 as the default python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip 1 && \
    ln -s /usr/bin/python3.9 /usr/bin/python

RUN python --version
RUN pip --version

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu113
RUN python -m unidic download
RUN python -m nltk.downloader averaged_perceptron_tagger_eng

COPY main.py ./
COPY src/ src/

EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--log-level", "info"]