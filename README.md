# Lyra - Audio to LRC Converter

Lyra is an open-source command-line tool that converts audio files to LRC (synchronized lyrics) format using speech-to-text transcription. It supports both Whisper and Google Gemini models for transcription, and it can isolate vocals from the audio using Demucs.

## Features

- Automatic speech-to-text transcription using either:
  - Whisper large-v3-turbo model
  - Google Gemini 2.5 Pro model (default)
- Automatic vocal isolation using Demucs
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

With metadata, eLRC extension:

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
* `--model, -m`: Model to use for transcription (choices: "whisper", "gemini", default: "gemini")
* `--prompt, -p`: Initial prompt text to guide transcription
* `--elrc`: Enable enhanced LRC format with word-level timestamps
* `--output, -o`: Output file path (default: output.lrc)
* `--title, -ti`: Song title
* `--artist, -ar`: Artist name
* `--album, -al`: Album name
* `--lyricist, -lr`: Lyricist name
* `--no-vocal-isolation`: Skip vocal isolation step

## Accuracy

While Demucs helps to isolate vocals and Whisper/Gemini provides high-quality transcription, the output will need to be reviewed and edited, especially if there are:
- Heavy effects on vocals
- Multiple overlapping voices

You can use the `--prompt` argument to guide the transcription process by providing the lyrics or an example of how it should be transcribed

You can also use Gemini as it hallucinates less but requires an API key