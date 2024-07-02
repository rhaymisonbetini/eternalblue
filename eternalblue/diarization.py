import torch
import torchaudio
import uuid
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from eternalblue.conversor import Conversor
from eternalblue.utils import OUTPUT_PATH


class Diarization:
    def __init__(self, hg_token: str):
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hg_token)
        device = torch.device("cuda")
        self.pipeline.to(device)
        self.conversor = Conversor()

    def diarize(self, audio_path, num_speakers) -> str | None:
        try:
            waveform, sample_rate = torchaudio.load(audio_path)
            with ProgressHook() as hook:
                diarization = self.pipeline({"waveform": waveform, "sample_rate": sample_rate},
                                            num_speakers=num_speakers,
                                            hook=hook)
                output_filename = f"{uuid.uuid4().hex}"
                with open(OUTPUT_PATH + f"/{output_filename}", 'w') as f:
                    for turn, _, speaker in diarization.itertracks(yield_label=True):
                        start_time = turn.start
                        duration = turn.end - turn.start
                        f.write(f"SPEAKER audio 1 {start_time:.3f} {duration:.3f} <NA> <NA> {speaker} <NA> <NA>\n")
                return output_filename
        except Exception as e:
            print(e)
            return None
