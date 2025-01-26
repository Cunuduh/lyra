# Lyra - Audio to LRC Converter

Lyra is an open-source command-line tool that converts audio files to LRC (synchronized lyrics) format using the Whisper automatic speech recognition model.

## Features

- Automatic speech-to-text transcription using Whisper large-v3 model
- Supports standard LRC and enhanced LRC (eLRC) formats 
- GPU acceleration when available (CUDA)
- Metadata support (title, artist, album, lyricist)
- Word-level timestamp accuracy

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Basic usage:

```bash
python cli.py audio_file.mp3
```

With metadata and eLRC extension:

```bash
python cli.py audio_file.mp3 --elrc \
    --title "Song Title" \
    --artist "Artist Name" \
    --album "Album Name" \
    --lyricist "Lyricist Name" \
    --output lyrics.lrc
```

### Arguments

* `audio_path`: Path to the audio file (required)
* `--elrc`: Enable enhanced LRC format with word-level timestamps
* `--output, -o`: Output file path (default: output.lrc)
* `--title, -ti`: Song title
* `--artist, -ar`: Artist name
* `--album, -al`: Album name
* `--lyricist, -lr`: Lyricist name