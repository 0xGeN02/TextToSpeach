from google.cloud import speech_v1 as speech

def transcribe_external(audio_path: str, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code,
    )
    response = client.recognize(config=config, audio=audio)
    return " ".join(result.alternatives[0].transcript for result in response.results)