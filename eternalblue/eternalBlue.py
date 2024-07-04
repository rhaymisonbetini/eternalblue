import os
import json
import torchaudio
import torchaudio.transforms as T
from eternalblue.diarization import Diarization
from eternalblue.transcription import Transcription
from eternalblue.utils import OUTPUT_PATH, AUDIOS_PATH, TRANSCRIPTION_PATH
import warnings

warnings.filterwarnings("ignore")


def create_directories():
    base_dir = os.path.join(os.path.dirname(__file__), 'public')
    sub_dirs = ['audios', 'outputs', 'transcriptions']

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for sub_dir in sub_dirs:
        dir_path = os.path.join(base_dir, sub_dir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


class EternalBlue:
    def __init__(self, hg_token: str, language: str, model: str = "openai/whisper-large-v3"):
        self.hg_token = hg_token
        self.language = language
        self.model = model
        create_directories()

    def diarize(self, audio_path: str, num_speakers=2):

        if not audio_path.endswith('.wav'):
            raise ValueError("Only .wav files are accepted")

        diarizer = Diarization(self.hg_token)

        waveform, sample_rate = torchaudio.load(audio_path)

        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0)

        resampler = T.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)
        waveform = waveform.squeeze()

        base_name = os.path.basename(audio_path)
        new_audio_path = os.path.join(AUDIOS_PATH, f"converted_{base_name}")

        torchaudio.save(new_audio_path, waveform.unsqueeze(0), 16000)

        audio_name = diarizer.diarize(new_audio_path, num_speakers)

        if audio_name is not None:
            transcriptor = Transcription(self.model, self.language)
            output_json = transcriptor.generate_transcription(new_audio_path, audio_name, self.language)
            with open(output_json, 'r', encoding='utf-8') as arquivo:
                pure_json = json.load(arquivo)
            os.remove(output_json)
            os.remove(OUTPUT_PATH + f"/{audio_name}")
            os.remove(new_audio_path)
            return pure_json

    @staticmethod
    def clear_cache():
        paths = [OUTPUT_PATH, AUDIOS_PATH, TRANSCRIPTION_PATH]
        for path in paths:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.exists(file_path):
                    os.remove(file_path)
