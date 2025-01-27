from faster_whisper import WhisperModel
import torch
from ..core.audio_processor import isolate_vocals

class Whisper:
    def __init__(self, model_name="large-v3"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.model = WhisperModel(
            model_size_or_path=model_name,
            device=device,
            compute_type="int8"
        )
    
    def transcribe(self, audio_path):
        print("Isolating vocals...")
        vocals = isolate_vocals(audio_path)
        print("Transcribing...")
        segments, _ = self.model.transcribe(
            audio=vocals,
            word_timestamps=True,
            hallucination_silence_threshold=1.5,
            log_prob_threshold=-0.75,
            beam_size=5,
            patience=2,
            log_progress=True
        )
        result = list(segments)
        return result