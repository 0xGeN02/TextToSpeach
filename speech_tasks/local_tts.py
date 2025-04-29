import pyttsx3


def speak_local(text: str):
    """
    Speak the given text using the local TTS engine.
    This function uses the pyttsx3 library to perform text-to-speech synthesis.
        This function uses the pyttsx3 library to convert text to speech.
    It initializes the text-to-speech engine, speaks the provided text,
    and waits for the speech to finish before returning.
"""
    engine = pyttsx3.init()

    engine.save_to_file(text, "../audio/output/local_tts.mp3")
    engine.runAndWait()
