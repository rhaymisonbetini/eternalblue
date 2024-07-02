import noisereduce as nr
import librosa
from pydub import AudioSegment
from pydub.effects import normalize
import soundfile as sf


class Conversor:
    def __init__(self):
        pass

    @staticmethod
    def convert_mp4_to_wav(audio_path: str) -> None:
        audio = AudioSegment.from_file(audio_path + "/consulta.mp4", "mp4")
        start_time_ms = 0
        end_time_ms = 1 * 60 * 1000 + 30 * 1000
        trimmed_audio = audio[start_time_ms:end_time_ms]
        trimmed_audio.export(audio_path + "/consulta.wav", format="wav")

    @staticmethod
    def split_audio(audio_path):
        audio = AudioSegment.from_file(audio_path + "/consulta.wav")
        segment_duration = 30 * 1000
        for i in range(3):
            start_time = i * segment_duration
            end_time = start_time + segment_duration
            segment = audio[start_time:end_time]
            segment.export(f"{audio_path}/segment_{i + 1}.wav", format="wav")

    @staticmethod
    def normalize(audio_path: str) -> None:
        audio, sr = librosa.load(audio_path + "/consulta.wav", sr=None)
        sr = int(sr)
        audio_clean = nr.reduce_noise(y=audio, sr=sr)
        sf.write(audio_path + "/consulta2.wav", audio_clean, sr)

        audio = AudioSegment.from_file(audio_path + "/consulta2.wav")
        normalized_audio = normalize(audio)
        normalized_audio.export(audio_path + "/consulta2.wav", format="wav")

        audio, sr = librosa.load(audio_path + "/consulta2.wav", sr=None)
        audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        sf.write(audio_path + "/consulta_remaster.wav", audio_resampled, 16000)

