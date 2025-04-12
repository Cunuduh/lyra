import torch
import torchaudio
from demucs.pretrained import get_model
from demucs.apply import apply_model

def downmix(wav: torch.Tensor) -> torch.Tensor:
    """
    Downmix the input audio to stereo using ITU-R BS.775 standard coefficients.
    """
    num_channels = wav.shape[0]
    
    if num_channels == 1:
        return wav.repeat(2, 1)
    elif num_channels == 2:
        return wav
    elif num_channels == 5: 
        # 5.0 surround (FL, FR, FC, BL, BR) to stereo
        # L = FL + 0.707*FC + 0.707*BL
        # R = FR + 0.707*FC + 0.707*BR
        return torch.stack([
            wav[0] + 0.707 * wav[2] + 0.707 * wav[3],
            wav[1] + 0.707 * wav[2] + 0.707 * wav[4]
        ])
    elif num_channels == 6:
        # 5.1 surround (FL, FR, FC, LFE, BL, BR) to stereo
        # L = FL + 0.707*FC + 0.707*BL
        # R = FR + 0.707*FC + 0.707*BR
        return torch.stack([
            wav[0] + 0.707 * wav[2] + 0.707 * wav[4],
            wav[1] + 0.707 * wav[2] + 0.707 * wav[5]
        ])
    else:
        return wav[:2]
    
def isolate_vocals(audio_path: str) -> str:
    """
    Isolate vocals from the input audio file using Demucs model and save the output to a temporary file.
    """
    model = get_model('htdemucs_ft')
    model.eval()

    wav, sr = torchaudio.load(audio_path)

    if sr != 44100:
        wav = torchaudio.functional.resample(wav, sr, 44100)
        sr = 44100

    if wav.shape[0] != 2:
        wav = downmix(wav)

    with torch.no_grad():
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        sources = apply_model(model, wav.unsqueeze(0), device=device)

    vocals = sources[0, 3].mean(dim=0, keepdim=True)

    vocals = torchaudio.functional.highpass_biquad(vocals, sr, 200)
    vocals = torchaudio.functional.lowpass_biquad(vocals, sr, 3000)

    temp_path = 'temp_vocals.wav'
    torchaudio.save(temp_path, vocals, sr)
    
    return temp_path