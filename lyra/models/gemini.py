import os
from typing import Optional, Iterator
from google import genai
from ..core.audio_processor import isolate_vocals

class Gemini:
    def __init__(self, model_name: str = "gemini-2.5-pro-exp-03-25"):
        """
        Initialize the Gemini model with the specified model name and API key.
        """
        api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        self.model_name: str = model_name
        self.client: genai.Client = genai.Client(api_key=api_key)
        
        self.standard_prompt_base: str = "Please transcribe the given song into .LRC format with precision to the centisecond ([MM:SS.CC]). Only depict silent/instrumental sections as \"♫\" if they are longer than 10 seconds. {isolation_note}\n\nEach lyric line should be capitalized at the beginning, but there should be no full stops. Other punctuation like question marks, commas, colons, semicolons, exclamation marks are allowed if they make sense. For example:\n\n[00:00.00] When the truth is found to be lies\n[00:06.47] And all the joy within you dies\n[00:13.34] Don't you want somebody to love?\n\nDO NOT output anything else other than the file's contents. DO NOT wrap the output in formatting such as \"```\"."
        
        self.elrc_prompt_base: str = "Please transcribe the given song into enhanced LRC format with word-level timestamps. For each line, provide the line timestamp followed by individual word timestamps in the format: [MM:SS.CC] <MM:SS.CC> word1 <MM:SS.CC> word2 <MM:SS.CC> word3. Only depict silent/instrumental sections as \"♫\" if they are longer than 10 seconds. {isolation_note}\n\nEach lyric line should be capitalized at the beginning, but there should be no full stops. Other punctuation like question marks, commas, colons, semicolons, exclamation marks are allowed if they make sense. For example:\n\n[00:00.00] <00:00.04> When <00:00.16> the <00:00.82> truth <00:01.29> is <00:01.63> found <00:03.09> to <00:03.37> be <00:05.92> lies \n[00:06.47] <00:07.67> And <00:07.94> all <00:08.36> the <00:08.63> joy <00:10.28> within <00:10.53> you <00:13.09> dies \n[00:13.34] <00:14.32> Don't <00:14.73> you <00:15.14> want <00:15.57> somebody <00:16.09> to <00:16.46> love\n\nDO NOT output anything else other than the file's contents. DO NOT wrap the output in formatting such as \"```\"."
    def transcribe(self, audio_path: str, isolate: bool = True, elrc: bool = False, prompt: Optional[str] = None) -> Iterator:
        """
        Transcribe the given audio file using the Gemini model.
        If isolate is True, vocals will be isolated from the audio before transcription.
        If elrc is True, generate enhanced LRC format with word-level timestamps.
        If prompt is provided, it will be used as additional guidance for transcription.
        """
        vocals_path: str = audio_path
        isolation_note: str = ""
        
        if isolate:
            print("Isolating vocals...")
            vocals_path = isolate_vocals(audio_path)
            isolation_note = "The vocals are isolated in the audio for easier transcription."
        
        if elrc:
            base_prompt = self.elrc_prompt_base.format(isolation_note=isolation_note)
        else:
            base_prompt = self.standard_prompt_base.format(isolation_note=isolation_note)
            
        # add user prompt if provided
        final_prompt = base_prompt
        if prompt:
            final_prompt = f"{base_prompt}\n\nAdditional guidance: {prompt}"
            
        vocal_file = self.client.files.upload(file=vocals_path)
        
        print("Transcribing...")
        for chunk in self.client.models.generate_content_stream(
            model=self.model_name,
            contents=[
                final_prompt,
                vocal_file
            ]
        ):
            yield chunk






