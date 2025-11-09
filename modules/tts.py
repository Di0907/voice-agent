# modules/tts.py
import edge_tts, os, time, asyncio


DEFAULT_VOICE = "en-US-AriaNeural"   
DEFAULT_RATE  = "+0%"
DEFAULT_PITCH = "+0Hz"


async def synthesize_mp3_async(
    text: str,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH,
) -> bytes:
    communicator = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    tmp = f"edge_tts_{int(time.time()*1000)}.mp3"
    await communicator.save(tmp)
    try:
        with open(tmp, "rb") as f:
            return f.read()
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass
