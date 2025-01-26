def generate(metadata, segments, elrc=False):
    lines = [f"[{key}: {value}]" for key, value in metadata.items() if value]
    
    merged_segments = []
    skip_next = False
    
    for i in range(len(segments)):
        if skip_next:
            skip_next = False
            continue

        seg = segments[i]
        words = list(seg.words)
        
        timestamps = {}
        for index, w in enumerate(words):
            timestamps.setdefault(w.start, []).append(index)
            
        remove_indices = set()
        for indices in timestamps.values():
            if len(indices) > 1:
                for index in indices:
                    remove_indices.add(index)
                    if index > 0:
                        remove_indices.add(index - 1)
        
        words = [w for i, w in enumerate(words) if i not in remove_indices]
        
        if remove_indices and i + 1 < len(segments):
            words.extend(segments[i + 1].words)
            skip_next = True
            
        seg.words = words
        merged_segments.append(seg)
    
    for segment in merged_segments:
        start = format_timestamp(segment.start)
        if not elrc:
            text = " ".join(w.word.strip() for w in segment.words)
            line = f"[{start}] {text}"
        else:
            timestamped_word = " ".join(f"<{format_timestamp(word.start)}> {word.word.strip()}" for word in segment.words)
            line = f"[{start}] {timestamped_word}"
        print(line)
        lines.append(line)
        
    return "\n".join(lines)

def format_timestamp(seconds: float) -> str:
    minutes = int(seconds // 60)
    seconds_remainder = seconds % 60
    return f"{minutes:02d}:{seconds_remainder:06.3f}"[:-1]  # [mm:ss.cc]