nohup tensorboard --logdir=/app/recipes/dominik_DE/ --bind_all > /dev/null 2>&1 &
nohup jupyter notebook --ip=0.0.0.0 --port=8888 --notebook-dir=/app/notebooks/dataset_analysis --allow-root --no-browser > /dev/null 2>&1 &
python3 /app/TTS/bin/train_tts.py --config_path /app/recipes/dominik_DE/config.json
#tail -f /dev/null