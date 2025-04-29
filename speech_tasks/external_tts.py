from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from gtts import gTTS
import os

def synthesize_external(text: str, output_path: str, lang: str = "en", engine: str = "elevenlabs", **kwargs):
    """
    Synthesize speech using an external TTS engine.
    Currently supports gTTS and ElevenLabs.
    
    Parameters:
    - text (str): The text to synthesize.
    - output_path (str): The path to save the synthesized audio file.
    - lang (str): The language code for the TTS engine (default: "en").
    - engine (str): The TTS engine to use ("gtts" or "elevenlabs").
    - **kwargs: Additional arguments for the TTS engine.
    
    Returns:
    - None: The synthesized audio is saved to the specified output path.
    """
    if engine == "gtts":
        # Use gTTS for text-to-speech synthesis
        tts = gTTS(text=text, lang=lang, slow=False, **kwargs)
        tts.save(output_path)

    elif engine == "elevenlabs":
        # Load environment variables
        load_dotenv()

        client = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
        )
        audio_gen = client.text_to_speech.convert(
            text="Hello from ElevenLabs TTS!, It's a pleasure to meet you!",
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        # Save the audio file
        with open(output_path, "wb") as f:
            for chunk in audio_gen:
                f.write(chunk)
