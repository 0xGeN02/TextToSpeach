import os
from gtts import gTTS
try:
    from elevenlabslib import ElevenLabsUser
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False


def synthesize_external(text: str, output_path: str, lang: str = "en", engine: str = "gtts", **kwargs):
    if engine == "gtts":
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
    elif engine == "elevenlabs":
        if not ELEVENLABS_AVAILABLE:
            raise ImportError("Please install elevenlabslib: poetry add elevenlabslib")
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise EnvironmentError("Set ELEVENLABS_API_KEY for ElevenLabs authentication.")
        user = ElevenLabsUser(api_key)
        voice_name = kwargs.get("voice_name", None)
        if not voice_name:
            raise ValueError("Provide voice_name for ElevenLabs TTS.")
        voices = user.get_available_voices()
        voice = next((v for v in voices if v.name == voice_name), None)
        if not voice:
            raise ValueError(f"Voice '{voice_name}' not found in ElevenLabs account.")
        voice.generate_and_save_audio(text=text, file_path=output_path)
    else:
        raise ValueError(f"Unsupported TTS engine: {engine}")
