ARG BASE=nvidia/cuda:11.8.0-base-ubuntu22.04
FROM ${BASE}

RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y git
RUN apt-get install -y --no-install-recommends gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install llvmlite --ignore-installed
RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
RUN python3 -m pip install --upgrade pip && \
    pip install pip setuptools wheel --upgrade
RUN pip install notebook
RUN rm -rf /root/.cache/pip

WORKDIR /app
RUN git clone https://github.com/coqui-ai/TTS.git /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 ./setup.py develop
COPY ./dominik_DE /app/recipes/dominik_DE


RUN nohup tensorboard --logdir=/app/recipes/dominik_DE/ --bind_all > /dev/null 2>&1 &
RUN nohup jupyter notebook --ip=0.0.0.0 --port=8888 --notebook-dir=/app/notebooks/dataset_analysis --allow-root --no-browser > /dev/null 2>&1 &

#CMD tail -f /dev/null
#CMD python3 /app/recipes/dominik_DE/train_tacotron_ddc.py
CMD python3 /app/TTS/bin/train_tts.py --config_path /app/recipes/dominik_DE/config.json

EXPOSE 6006
EXPOSE 8888