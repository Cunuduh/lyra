from faster_whisper import WhisperModel
import torch

class Whisper:
    def __init__(self, model_name="large-v3"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.model = WhisperModel(
            model_size_or_path=model_name,
            device=device,
            compute_type="int8"
        )
    
    def transcribe(self, audio_path):
        print("Transcribing...")
        segments, _ = self.model.transcribe(
            audio=audio_path,
            word_timestamps=True,
        )
        result = [segment for segment in segments]
        return result