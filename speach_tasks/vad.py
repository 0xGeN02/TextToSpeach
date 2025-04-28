import wave
import webrtcvad

def detect_speech_regions(audio_path: str, aggressiveness: int = 1):
    vad = webrtcvad.Vad(aggressiveness)
    wf = wave.open(audio_path, "rb")
    rate = wf.getframerate()
    frame_ms = 30
    frame_bytes = int(rate * frame_ms / 1000) * wf.getsampwidth()

    regions = []
    in_speech = False
    ms_index = 0

    while frame := wf.readframes(int(rate * frame_ms / 1000)):
        is_speech = vad.is_speech(frame, rate)
        t = ms_index * frame_ms
        if is_speech and not in_speech:
            start = t
            in_speech = True
        elif not is_speech and in_speech:
            regions.append((start, t))
            in_speech = False
        ms_index += 1
    wf.close()
    return regions
