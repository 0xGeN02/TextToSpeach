
import contextlib
import wave
import webrtcvad


def read_wave(path: str) -> tuple:
    """
    Reads a .wav file and returns the PCM data and sample rate.
    Args:
        path (str): Path to the .wav file.   
    Returns:
        tuple: PCM data and sample rate.
    Raises:
        ValueError: If the audio file is not mono, has an invalid sample width, or has an invalid sample rate.
        FileNotFoundError: If the audio file does not exist.
    """
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


def detect_speech_regions(audio_path: str) -> list:
    """
    Detect speech regions in an audio file using WebRTC VAD.
    Args:
        audio_path (str): Path to the audio file.
        frame_duration (int): Duration of each frame in milliseconds.
    Returns:
        list: List of speech regions in milliseconds.
    Raises:
        FileNotFoundError: If the audio file does not exist.
        ValueError: If the audio file is not mono, has an invalid sample width, or has an invalid sample rate.
    """
    audio, sample_rate = read_wave(audio_path)
    vad = webrtcvad.Vad(3)  # Aggressiveness 0-3
    frame_duration = 30  # ms
    frame_size = int(sample_rate * frame_duration / 1000) * 2
    frames = [audio[i:i + frame_size] for i in range(0, len(audio), frame_size)]

    speech_regions = []
    timestamp = 0
    for frame in frames:
        if len(frame) != frame_size:
            continue  # Salta frames incompletos
        is_speech = vad.is_speech(frame, sample_rate)
        if is_speech:
            speech_regions.append(timestamp)
        timestamp += frame_duration
    return speech_regions
