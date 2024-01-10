nohup tensorboard --logdir=/app/recipes/dominik_DE/ --bind_all > /dev/null 2>&1 &
nohup jupyter notebook --ip=0.0.0.0 --port=8888 --notebook-dir=/app/notebooks/dataset_analysis --allow-root --no-browser > /dev/null 2>&1 &
if [ -n "$CONTINUE_PATH" ] && [ -n "$CONFIG_PATH" ]
then
  echo "Der Pfad ist: $CONTINUE_PATH"
  python3 /app/TTS/bin/train_tts.py --config_path $CONFIG_PATH --continue_path $CONTINUE_PATH
else
  echo "CONTINUE_PATH ist nicht gesetzt oder die config.json Datei existiert nicht"
  #python3 /app/recipes/dominik_DE/train_tacotron_ddc.py
  python3 /app/recipes/dominik_DE/train_vits.py
fi