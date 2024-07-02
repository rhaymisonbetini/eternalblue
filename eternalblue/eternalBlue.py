import os
import json
from eternalblue.Diarization import Diarization
from eternalblue.Transcription import Transcription
from eternalblue.utils import OUTPUT_PATH


class EternalBlue:
    def __init__(self, hg_token: str, language: str, model: str = "openai/whisper-large-v3"):
        self.hg_token = hg_token
        self.language = language
        self.model = model

    def diarize(self, audio_path: str, num_speakers=2):
        diarizer = Diarization(self.hg_token)
        audio_name = diarizer.diarize(audio_path, num_speakers)
        if audio_name is not None:
            transcriptor = Transcription(self.model)
            output_json = transcriptor.generate_transcription(audio_path, audio_name, self.language)
            with open(output_json, 'r', encoding='utf-8') as arquivo:
                pure_json = json.load(arquivo)
            os.remove(output_json)
            os.remove(OUTPUT_PATH + f"/{audio_name}")
            return pure_json
