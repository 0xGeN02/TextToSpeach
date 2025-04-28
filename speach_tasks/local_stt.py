import os
import wave
import json
import vosk


def transcribe_local(audio_path: str) -> str:
    model_path = os.getenv("VOSK_MODEL_PATH")
    if not model_path:
        raise EnvironmentError("VOSK_MODEL_PATH not set")

    model = vosk.Model(model_path)
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        raise ValueError("Audio file must be WAV format Mono PCM")

    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    result_text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result_text += res.get('text', '') + " "

    res = json.loads(rec.FinalResult())
    result_text += res.get('text', '')

    return result_text.strip()
