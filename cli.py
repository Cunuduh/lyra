import argparse
import av
from lyra.models.faster_whisper import Whisper
from lyra.core.lrc_generator import generate

def main():
    parser = argparse.ArgumentParser(description="Lyra: Audio to LRC Converter")
    parser.add_argument("audio_path", help="Path to audio file")
    parser.add_argument("--elrc", action="store_true", help="Use ELRC format")
    parser.add_argument("--output", "-o", default="output.lrc", help="Output file")
    parser.add_argument("--title", "-ti", default="", help="Song title")
    parser.add_argument("--artist", "-ar", default="", help="Artist name")
    parser.add_argument("--album", "-al", default="", help="Album name")
    parser.add_argument("--lyricist", "-lr", default="", help="Lyricist name")
    
    args = parser.parse_args()

    whisper = Whisper()

    segments = whisper.transcribe(args.audio_path)

    metadata = {
        "ti": args.title,
        "ar": args.artist,
        "al": args.album,
        "lr": args.lyricist,
        "re": "Lyra - Audio to LRC Converter",
        "length": format_duration(get_audio_duration(args.audio_path))
    }
    
    lrc_content = generate(metadata, segments, elrc=args.elrc)
    
    with open(args.output, "w") as f:
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