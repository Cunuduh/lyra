import av
import torch
import torchaudio
from demucs.pretrained import get_model
from demucs.apply import apply_model
def downmix(wav):
    num_channels = wav.shape[0]
    
    if num_channels == 1:
        return wav.repeat(2, 1)
    elif num_channels == 2:
        return wav
    elif num_channels == 5:
        # (FL, FR, FC, BL, BR)
        return torch.stack([
            wav[0] + 0.707*wav[2] + 0.707*wav[3],
            wav[1] + 0.707*wav[2] + 0.707*wav[4]
        ])
    elif num_channels == 6:
        # (FL, FR, FC, LFE, BL, BR)
        return torch.stack([
            wav[0] + 0.707*wav[2] + 0.707*wav[4],
            wav[1] + 0.707*wav[2] + 0.707*wav[5]
        ])
    else:
        return torch.stack([wav.mean(dim=0), wav.mean(dim=0)])
    
def isolate_vocals(audio_path):
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
    window_size = int(sr * 0.02)
    energy = torch.norm(vocals.unfold(-1, window_size, window_size), dim=-1)
    mask = energy > energy.max() * 0.05

    vocals_filtered = torch.zeros_like(vocals)
    for i, keep in enumerate(mask.squeeze()):
        if keep:
            start = i * window_size
            end = start + window_size
            vocals_filtered[..., start:end] = vocals[..., start:end]
    temp_path = 'temp_vocals.wav'
    torchaudio.save(temp_path, vocals, sr)
    
    return temp_path