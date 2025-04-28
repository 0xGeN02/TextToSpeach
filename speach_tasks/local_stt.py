import wave
from vosk import Model, KaldiRecognizer

# Ensure you have downloaded a Vosk model and set VOSK_MODEL_PATH
# export VOSK_MODEL_PATH="/path/to/vosk-model-small-en-us-0.15"

def transcribe_local(audio_path: str) -> str:
    model_path = os.getenv("VOSK_MODEL_PATH")
    if not model_path:
        raise EnvironmentError("Please set VOSK_MODEL_PATH environment variable.")

    model = Model(model_path)
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in (8000, 16000, 32000, 48000):
        raise ValueError("Audio file must be WAV mono PCM.")

    rec = KaldiRecognizer(model, wf.getframerate())
    result = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part = rec.Result()
            result.append(part)
    result.append(rec.FinalResult())
    return " ".join(result)
