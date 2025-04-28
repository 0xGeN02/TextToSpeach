import os
from speech_tasks.local_stt import transcribe_local
from speech_tasks.local_tts import speak_local
from speech_tasks.external_stt import transcribe_external
from speech_tasks.external_tts import synthesize_external
from speech_tasks.vad import detect_speech_regions


def main():
    """
    Main function to demonstrate the usage of local and external STT and TTS.
    This function performs the following tasks:
    1. Transcribe audio using local STT.
    2. Synthesize speech using local TTS.
    3. Transcribe audio using external STT.
    4. Synthesize speech using external TTS (gTTS).
    5. Synthesize speech using external TTS (ElevenLabs).
    6. Detect speech regions in the audio file.
    """
    audio_file = "./audio/samples/sample.wav"

    # 1. Local STT
    print("[Local STT]", transcribe_local(audio_file))

    # 2. Local TTS
    speak_local("Hello from local TTS!")

    # 3. External (free) STT
    print("[External STT]", transcribe_external(audio_file))

    # 4. External (free) TTS via gTTS
    synthesize_external("Hello from free external TTS!", "./audio/output/tts_gtts.mp3", engine="gtts")
    print("Saved free TTS to tts_gtts.mp3")

    # 5. External TTS via ElevenLabs
    try:
        synthesize_external(
            "Hello from ElevenLabs TTS!", 
            "./audio/output/tts_elevenlabs.mp3", 
            engine="elevenlabs",
            voice_name=os.getenv("ELEVENLABS_VOICE", "alloy")
        )
        print("Saved ElevenLabs TTS to tts_elevenlabs.mp3")
    except Exception as e:
        print(f"ElevenLabs TTS failed: {e}")

    # 6. Voice Activity Detection
    regions = detect_speech_regions(audio_file)
    print("Speech regions (ms):", regions)


if __name__ == "__main__":
    main()
