import os
from speach_tasks.local_stt import transcribe_local
from speach_tasks.local_tts import speak_local
from speach_tasks.external_stt import transcribe_external
from speach_tasks.external_tts import synthesize_external
from speach_tasks.vad import detect_speech_regions


def main():
    audio_file = "./audio/sample.wav"

    # 1. Local STT
    print("[Local STT]", transcribe_local(audio_file))

    # 2. Local TTS
    speak_local("Hello from local TTS!")

    # 3. External (free) STT
    print("[External STT]", transcribe_external(audio_file))

    # 4. External (free) TTS via gTTS
    synthesize_external("Hello from free external TTS!", "tts_gtts.mp3", engine="gtts")
    print("Saved free TTS to tts_gtts.mp3")

    # 5. External TTS via ElevenLabs
    try:
        synthesize_external(
            "Hello from ElevenLabs TTS!", 
            "tts_elevenlabs.mp3", 
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
