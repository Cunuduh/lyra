def generate(metadata, segments, elrc=False):
    lines = [f"[{key}: {value}]" for key, value in metadata.items() if value]
    lines.append("")
    
    for segment in segments:
        start = format_timestamp(segment.start)
        if not elrc:
            text = " ".join(w.word.strip() for w in segment.words)
            line = f"[{start}] {text}"
        else:
            timestamped_word = " ".join(f"<{format_timestamp(word.start)}> {word.word.strip()}" for word in segment.words)
            line = f"[{start}] {timestamped_word}"
        lines.append(line)

    for line in lines:
        print(line)

    return "\n".join(lines)
def generate_gemini(metadata, gemini, args):
    result = ""
    for chunk in gemini.transcribe(args.audio_path):
        if not result:
            result = "\n".join(f"[{key}: {value}]" for key, value in metadata.items() if value)
            result += "\n\n"
            print(result, end="", flush=True)
        if chunk.text:
            result += chunk.text
            print(chunk.text, end="", flush=True)
    return result

def format_timestamp(seconds: float) -> str:
    minutes = int(seconds // 60)
    seconds_remainder = seconds % 60
    return f"{minutes:02d}:{seconds_remainder:06.3f}"[:-1]  # [mm:ss.cc]