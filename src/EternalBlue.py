from src.Diarization import Diarization
from src.Transcription import Transcription
import json


class EternalBlue:
    def __init__(self, hg_token: str, language: str):
        self.hg_token = hg_token
        self.language = language

    def diarize(self, audio_path: str, num_speakers=2):
        diarizer = Diarization(self.hg_token)
        audio_name = diarizer.diarize(audio_path, num_speakers)
        if audio_name is not None:
            transcriptor = Transcription()
            output_json = transcriptor.generate_transcription(audio_path, audio_name, self.language)
            pure_json = json.loads(output_json)
            return pure_json
