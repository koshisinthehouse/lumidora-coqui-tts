import os

from trainer import Trainer, TrainerArgs

from TTS.config.shared_configs import BaseAudioConfig
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.tacotron2_config import Tacotron2Config
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.tacotron2 import Tacotron2
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

# from TTS.tts.datasets.tokenizer import Tokenizer

output_path = os.path.dirname(os.path.abspath(__file__))

# init configs
dataset_config = BaseDatasetConfig(language="de_DE",
    formatter="ljspeech", meta_file_train="metadata.csv", path=os.path.join(output_path, "./")
)

# VOCABULARY PARAMETERS
    # if custom character set is not defined,
    # default set in symbols.py is used
    # "characters":{
    #     "pad": "_",
    #     "eos": "~",
    #  "bos": "^",
    #    "characters": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!'(),-.:;? ",
    #     "punctuations":"!'(),-.:;? ",
    #     "phonemes":"iyɨʉɯuɪʏʊeøɘəɵɤoɛœɜɞʌɔæɐaɶɑɒᵻʘɓǀɗǃʄǂɠǁʛpbtdʈɖcɟkɡqɢʔɴŋɲɳnɱmʙrʀⱱɾɽɸβfvθðszʃʒʂʐçʝxɣχʁħʕhɦɬɮʋɹɻjɰlɭʎʟˈˌːˑʍwɥʜʢʡɕʑɺɧɚ˞ɫ"
    # },



# mel_fmin=0.0,
audio_config = BaseAudioConfig(
    sample_rate=44100,
    do_trim_silence=True,
    trim_db=60.0,
    signal_norm=False,
    mel_fmin=50,
    mel_fmax=8000,
    spec_gain=1.0,
    log_func="np.log",
    ref_level_db=20,
    preemphasis=0.0,
)

config = Tacotron2Config(  # This is the config that is saved for the future use
    run_name="Domoskanonos_Tacotron2_ddc",
    run_description="Domoskanonos Tacotron2 DDC model with Dominik's dataset",
    save_step=2000,
    save_all_best=True,
    audio=audio_config,
    batch_size=16, # BS of 40 and max length of 10s will use about 20GB of GPU memory
    eval_batch_size=16,
    num_loader_workers=8,
    num_eval_loader_workers=8,
    run_eval=True,
    test_delay_epochs=-1,
    r=7,
    gradual_training= [[0, 7, 16], [10000, 5, 16], [50000, 3, 16], [130000, 2, 8], [290000, 1, 8]],
    double_decoder_consistency=True,
    epochs=1000,
    text_cleaner="phoneme_cleaners",
    use_phonemes=True,
    phoneme_language="de",
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    precompute_num_workers=8,
    print_step=25,
    print_eval=True,
    #max_audio_len=44100 * 10,
    mixed_precision=False,
    output_path=output_path,
    datasets=[dataset_config],
    test_sentences=[
        "Es hat mich viel Zeit gekostet ein Stimme zu entwickeln, jetzt wo ich sie habe werde ich nicht mehr schweigen.",
        "Sei eine Stimme, kein Echo.",
        "Es tut mir Leid David. Das kann ich leider nicht machen.",
        "Dieser Kuchen ist großartig. Er ist so lecker und feucht.",
        "Vor dem 22. November 1963.",
    ],
)

# init audio processor
ap = AudioProcessor(**config.audio.to_dict())

# INITIALIZE THE AUDIO PROCESSOR
# Audio processor is used for feature extraction and audio I/O.
# It mainly serves to the dataloader and the training loggers.
ap = AudioProcessor.init_from_config(config)

# INITIALIZE THE TOKENIZER
# Tokenizer is used to convert text to sequences of token IDs.
# If characters are not defined in the config, default characters are passed to the config
tokenizer, config = TTSTokenizer.init_from_config(config)

# LOAD DATA SAMPLES
# Each sample is a list of ```[text, audio_file_path, speaker_name]```
# You can define your custom sample loader returning the list of samples.
# Or define your custom formatter and pass it to the `load_tts_samples`.
# Check `TTS.tts.datasets.load_tts_samples` for more details.
train_samples, eval_samples = load_tts_samples(
    dataset_config,
    eval_split=True,
    eval_split_max_size=config.eval_split_max_size,
    eval_split_size=config.eval_split_size,
)

# INITIALIZE THE MODEL
# Models take a config object and a speaker manager as input
# Config defines the details of the model like the number of layers, the size of the embedding, etc.
# Speaker manager is used by multi-speaker models.
model = Tacotron2(config, ap, tokenizer, speaker_manager=None)

# init the trainer and 🚀
trainer = Trainer(
    TrainerArgs(), config, output_path, model=model, train_samples=train_samples, eval_samples=eval_samples
)
trainer.fit()
