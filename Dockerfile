ARG BASE=nvidia/cuda:11.8.0-base-ubuntu22.04
FROM ${BASE}

RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y git
RUN apt-get install -y --no-install-recommends gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install llvmlite --ignore-installed

# Install Dependencies:
RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
RUN rm -rf /root/.cache/pip


# CLONE TTS REPOSITORY:
RUN git clone https://github.com/coqui-ai/TTS.git /app


# Copy TTS repository contents:
WORKDIR /app

RUN python3 -m pip install --upgrade pip && \
    pip install pip setuptools wheel --upgrade

# Kopieren Sie die Anforderungsdatei in den Container
#COPY requirements.txt ./

# Installieren Sie alle in requirements.txt aufgeführten Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install notebook

# Führen Sie setup.py aus
RUN python3 ./setup.py develop

COPY ./dominik_DE /app/recipes/dominik_DE

#ENTRYPOINT ["tts"]
CMD tail -f /dev/null

EXPOSE 8888