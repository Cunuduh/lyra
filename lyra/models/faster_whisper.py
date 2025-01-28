from faster_whisper import WhisperModel
import torch
from ..core.audio_processor import isolate_vocals

class Whisper:
    def __init__(self, model_name="large-v3-turbo"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.model = WhisperModel(
            model_size_or_path=model_name,
            device=device,
            compute_type="int8"
        )
    
    def transcribe(self, audio_path, prompt=None):
        print("Isolating vocals...")
        vocals = isolate_vocals(audio_path)
        print("Transcribing...")
        segments, _ = self.model.transcribe(
            audio=vocals,
            word_timestamps=True,
            initial_prompt=prompt,
            hallucination_silence_threshold=1.0,
            log_prob_threshold=-0.693,
            beam_size=5,
            patience=2.0,
            temperature=0.0,
            log_progress=True
        )
        result = list(segments)
        return result