from typing import List, Dict, Optional
import argparse
from lyra.models.gemini import Gemini

def generate(metadata: Dict[str, Optional[str]], segments: List, elrc: bool = False) -> str:
    lines: List[str] = [f"[{key}: {value}]" for key, value in metadata.items() if value]
    lines.append("")
    
    for segment in segments:
        start: str = format_timestamp(segment.start)
        if not elrc:
            text: str = " ".join(w.word.strip() for w in segment.words)
            line: str = f"[{start}] {text}"
        else:
            timestamped_word: str = " ".join(f"<{format_timestamp(word.start)}> {word.word.strip()}" for word in segment.words)
            line = f"[{start}] {timestamped_word}"
        lines.append(line)

    for line in lines:
        print(line)

    return "\n".join(lines)

def generate_gemini(metadata: Dict[str, Optional[str]], gemini: Gemini, args: argparse.Namespace, isolate: bool = True) -> str:
    result: str = ""
    for chunk in gemini.transcribe(args.audio_path, isolate=isolate, elrc=args.elrc, prompt=args.prompt if args.prompt else None):
        if not result:
            result = "\n".join(f"[{key}: {value}]" for key, value in metadata.items() if value)
            result += "\n\n"
            print(result, end="", flush=True)
        if chunk.text:
            result += chunk.text
            print(chunk.text, end="", flush=True)
    return result

def format_timestamp(seconds: float) -> str:
    minutes: int = int(seconds // 60)
    seconds_remainder: float = seconds % 60
    return f"{minutes:02d}:{seconds_remainder:06.3f}"[:-1]  # [mm:ss.cc]