import torch
import json
import os
from transformers import pipeline
from transformers import WhisperForConditionalGeneration
from transformers import WhisperProcessor
from pydub import AudioSegment
from eternalblue.utils import TRANSCRIPTION_PATH, OUTPUT_PATH, AUDIOS_PATH


def round_times(segments):
    rounded_segments = []
    for segment in segments:
        speaker_id, start_time, end_time = segment
        start_time_rounded = start_time
        end_time_rounded = end_time
        rounded_segments.append((speaker_id, start_time_rounded, end_time_rounded))
    return rounded_segments


def read_rttm(file_path):
    segments = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            speaker_id = parts[7]
            start_time = float(parts[3])
            end_time = start_time + float(parts[4])
            segments.append((speaker_id, start_time, end_time))
    return segments


class Transcription:
    def __init__(self, model: str, language: str):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model_id = model
        self.model = WhisperForConditionalGeneration.from_pretrained(
            self.model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.model.to(self.device)
        processor = WhisperProcessor.from_pretrained(self.model_id, language=language, task="transcribe")
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            batch_size=16,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )

    def generate_transcription(self, audio_path: str, audio_name: str, language: str) -> str:
        rttm_file_path = OUTPUT_PATH + f"/{audio_name}"
        segments = read_rttm(rttm_file_path)
        rounded_segments = round_times(segments)
        audio = AudioSegment.from_file(audio_path)

        name = audio_path.split("/")[-1]
        transcriptions_array = [{"metadata": [{"audioname": name, "time_type": "seconds"}]}]

        for i, segment in enumerate(rounded_segments):
            speaker_id, start, end = segment
            if end - start > 0.2:
                segment_audio = audio[start * 1000:end * 1000]  # Pydub works in milliseconds
                audio_name = f"{speaker_id}_segment_{i}.wav"
                output_path = os.path.join(AUDIOS_PATH, audio_name)
                segment_audio.export(output_path, format="wav")

                transcription = self.pipe(output_path,
                                          chunk_length_s=int(end - start) + 0.5,
                                          generate_kwargs={"language": language, "task": "transcribe"},
                                          )

                transcriptions_array.append({
                    "start": float(start),
                    "end": float(end),
                    "text": transcription["text"],
                    "speaker_id": speaker_id,
                })

                if os.path.exists(output_path):
                    os.remove(output_path)

        json_name = name.split(".")[0]
        output_file = TRANSCRIPTION_PATH + f"/{json_name}.json"
        with open(output_file, "w") as file:
            json.dump(transcriptions_array, file, ensure_ascii=False, indent=4)
        return output_file
