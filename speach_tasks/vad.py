
import contextlib
import wave
import webrtcvad


def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        if num_channels != 1:
            raise ValueError("Audio must be mono")
        sample_width = wf.getsampwidth()
        if sample_width != 2:
            raise ValueError("Sample width must be 2")
        sample_rate = wf.getframerate()
        if sample_rate not in (8000, 16000, 32000, 48000):
            raise ValueError("Invalid sample rate")
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


def detect_speech_regions(audio_path: str):
    audio, sample_rate = read_wave(audio_path)
    vad = webrtcvad.Vad(3)  # Aggressiveness 0-3
    frame_duration = 30  # ms
    frame_size = int(sample_rate * frame_duration / 1000) * 2
    frames = [audio[i:i + frame_size] for i in range(0, len(audio), frame_size)]

    speech_regions = []
    timestamp = 0
    for frame in frames:
        is_speech = vad.is_speech(frame, sample_rate)
        if is_speech:
            speech_regions.append(timestamp)
        timestamp += frame_duration
    return speech_regions
