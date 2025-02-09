# Lyra - Audio to LRC Converter

Lyra is an open-source command-line tool that converts audio files to LRC (synchronized lyrics) format using the Whisper automatic speech recognition model.

## Features

- Automatic speech-to-text transcription using either:
  - Whisper large-v3-turbo model (default)
  - Google Gemini 2.0 Pro model
- Automatic vocal isolation using Demucs
- Supports standard LRC and enhanced LRC (eLRC) formats (Whisper only)
- GPU acceleration when available (CUDA)
- Metadata support (title, artist, album, lyricist)
- Word-level timestamp accuracy (Whisper only)

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

With metadata, eLRC extension (Whisper only):

```bash
python cli.py audio_file.mp3 --elrc \
    --prompt "Initial prompt" \
    --title "Song Title" \
    --artist "Artist Name" \
    --album "Album Name" \
    --lyricist "Lyricist Name" \
    --output lyrics.lrc
```

### Arguments

* `audio_path`: Path to the audio file (required)
* `--model, -m`: Model to use for transcription (choices: "whisper", "gemini", default: "whisper")
* `--prompt, -p`: Initial prompt text to guide transcription
* `--elrc`: Enable enhanced LRC format with word-level timestamps
* `--output, -o`: Output file path (default: output.lrc)
* `--title, -ti`: Song title
* `--artist, -ar`: Artist name
* `--album, -al`: Album name
* `--lyricist, -lr`: Lyricist name

## Accuracy

While Demucs helps to isolate vocals and Whisper/Gemini provides high-quality transcription, the output will need to be reviewed and edited, especially if there are:
- Heavy effects on vocals
- Multiple overlapping voices

You can use the `--prompt` argument to guide Whisper's transcription process by providing the initial lyrics or an example of how it should be transcribed

You can also use Gemini as it hallucinates less but timestamps are not as accurate as Whisper