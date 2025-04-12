from faster_whisper import WhisperModel
import torch
from typing import List, Optional, Iterator 
from ..core.audio_processor import isolate_vocals

class Whisper:
    def __init__(self, model_name: str = "large-v3-turbo") -> None:
        """
        Initialize the Whisper model with the specified model name.
        """
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type: str = "float16" if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else "int8"

        self.model: WhisperModel = WhisperModel(
            model_size_or_path=model_name,
            device=device,
            compute_type=compute_type
        )
    def transcribe(self, audio_path: str, prompt: Optional[str] = None, isolate: bool = True) -> List:
        """
        Transcribe the given audio file using the Whisper model.
        The prompt is used to guide the transcription process.
        If isolate is True, vocals will be isolated from the audio before transcription.
        """
        vocals_path: str = audio_path
        if isolate:
            print("Isolating vocals...")
            vocals_path = isolate_vocals(audio_path)
        print("Transcribing...")
        segments_iterator: Iterator
        segments_iterator, _ = self.model.transcribe(
            audio=vocals_path,
            word_timestamps=True,
            initial_prompt=prompt,
            hallucination_silence_threshold=0.75,
            log_prob_threshold=-0.693,
            beam_size=5,
            patience=2.0,
            temperature=0.0,
            log_progress=True
        )
        result = list(segments_iterator)
        return result