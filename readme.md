# build image, no-cache
    docker build --no-cache -t my-tts-image .
    docker build -t my-tts-image .

# run container
    docker run -p 8888:8888 -p 6006:6006 -v "my-tts-image:/app/recipes/dominik_DE" --gpus 1 my-tts-image

# run container with CONTINUE_PATH
    docker run -p 8888:8888 -p 6006:6006 -v "my-tts-image:/app/recipes/dominik_DE" --gpus 1 --shm-size=2g -e CONTINUE_PATH='/app/recipes/dominik_DE/Domoskanonos_Tacotron2_ddc-January-09-2024_12+20PM-5dcc16d1' my-tts-image

# windows volume url
    \\wsl.localhost\docker-desktop-data\data\docker\volumes\my-tts-image\_data\

# look at 
    http://127.0.0.1:6006/
    http://127.0.0.1:8888/[TOKEN]


# Nützlihe Tools
    python3 /app/TTS/bin/find_unique_chars.py --config_path=/app/recipes/dominik_DE/config.json
    python3 /app/TTS/bin/find_unique_phonemes.py --config_path=/app/recipes/dominik_DE/config.json


# 16 gb GPU
     gradual_training=[[0, 6, 32], [10000, 4, 16], [50000, 3, 8], [100000, 2, 8]],

     gradual_training= [[0, 7, 32], [10000, 5, 32], [50000, 3, 32], [130000, 2, 16], [290000, 1, 8]]



# 8 GB GPU
            r=6,
    gradual_training=[[0, 6, 64], [10000, 4, 32], [50000, 3, 32], [100000, 2, 32]],




Synthezizen mit Checkpoint
python3 /app/TTS/bin/synthesize.py --model_path=[CHECKPOINT_PATH] --config_path=/app/recipes/dominik_DE/config.json --out_path=/app/recipes/dominik_DE/out --text="Das ist ein toller Text"


Für executable fertig trainierte Stimmen auszuführen:
pip3 install tts
