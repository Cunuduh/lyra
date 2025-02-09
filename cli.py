import argparse
import av
from lyra.models.faster_whisper import Whisper
from lyra.models.gemini import Gemini
from lyra.core.lrc_generator import generate, generate_gemini

def main():
    parser = argparse.ArgumentParser(description="Lyra: Audio to LRC Converter")
    parser.add_argument("audio_path", help="Path to audio file")
    parser.add_argument(
        "--model", "-m",
        choices=["whisper", "gemini"],
        default="whisper",
        help="Model to use for transcription (default: whisper)"
    )
    parser.add_argument("--prompt", "-p", default="", help="Initial prompt with lyrics text (Whisper only)")
    parser.add_argument("--elrc", action="store_true", help="Use ELRC format (Whisper only)")
    parser.add_argument("--output", "-o", default="output.lrc", help="Output file")
    parser.add_argument("--title", "-ti", default="", help="Song title")
    parser.add_argument("--artist", "-ar", default="", help="Artist name")
    parser.add_argument("--album", "-al", default="", help="Album name")
    parser.add_argument("--lyricist", "-lr", default="", help="Lyricist name") 
    args = parser.parse_args()
    
    metadata = {
        "ti": args.title,
        "ar": args.artist,
        "al": args.album,
        "lr": args.lyricist,
        "re": "Lyra - Audio to LRC Converter",
        "length": format_duration(get_audio_duration(args.audio_path))
    }
    if args.model == "whisper":
        whisper = Whisper()
        segments = whisper.transcribe(args.audio_path, prompt=args.prompt if args.prompt else None)
        lrc_content = generate(metadata, segments, elrc=args.elrc)
    elif args.model == "gemini":
        gemini = Gemini()
        lrc_content = generate_gemini(metadata, gemini, args)
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(lrc_content)

def get_audio_duration(audio_path):
    container = av.open(audio_path)
    duration = container.duration / av.time_base
    container.close()
    return duration

def format_duration(seconds: float) -> str:
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"

if __name__ == "__main__":
    main()