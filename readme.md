# build image, no-cache
    docker build --no-cache -t my-tts-image .

# run container
    docker run -d -p 8888:8888 -v "my-tts-image:/app/recipes/dominik_DE" --gpus 1 --shm-size=2g my-tts-image

# windows volume url
    \\wsl.localhost\docker-desktop-data\data\docker\volumes\my-tts-image\_data\

# run jupyter notebook
    jupyter notebook --ip=0.0.0.0 --port=8888 --notebook-dir=/app/notebooks/dataset_analysis --allow-root --no-browser

# run training
    python3 ./recipes/dominik_DE/train_tacotron_ddc.py



geht noch nicht
./compute_statistics.py config_path=/app/TTS/recipes/dominik_DE/metadata.csv out_path=/app/TTS/recipes/dominik_DE/out


cd Domoskanonos_Tacotron2_ddc-January-07-2024_06+10PM-5dcc16d1



Für executable fertig trainierte Stimmen auszuführen:
pip3 install tts
