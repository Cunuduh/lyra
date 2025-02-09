import os
from google import genai
from ..core.audio_processor import isolate_vocals

class Gemini:
    def __init__(self, model_name="gemini-2.0-pro-exp-02-05"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)
        self.prompt = "Please transcribe the given song into .LRC format with precision to the centisecond ([MM:SS.CC]). Depict silent/instrumental sections as \"♫\". The vocals are isolated in the audio for easier transcription.\n\nEach lyric line should be capitalized at the beginning, but there should be no full stops. Other punctuation like question marks, commas, colons, semicolons, exclamation marks are allowed if they make sense. For example:\n\n[00:00.00] When the truth is found to be lies\n[00:06.47] And all the joy within you dies\n[00:13.34] Don't you want somebody to love?\n\nDO NOT output anything else other than the file's contents. DO NOT wrap the output in formatting such as \"```\"."
    
    def transcribe(self, audio_path):
        print("Isolating vocals...")
        vocals = isolate_vocals(audio_path)
        vocal_file = self.client.files.upload(file=vocals)
        print("Transcribing...")
        for chunk in self.client.models.generate_content_stream(
            model=self.model_name,
            contents=[
                self.prompt,
                vocal_file
            ]
        ):
            yield chunk
        
        
        


        
                   