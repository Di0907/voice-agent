from faster_whisper import WhisperModel
import numpy as np
import io
import av

_asr = None

def load_asr(model_name: str = "small.en"):
    """
    Load faster-whisper ASR (CPU int8). Switch compute_type to "float32" if int8 not supported.
    """
    global _asr
    if _asr is None:
        _asr = WhisperModel(
            model_name,
            device="cpu",
            compute_type="int8",
        )
    return _asr

def _decode_to_mono16k(audio_bytes: bytes) -> np.ndarray:
    """
    Decode webm/ogg/mp3/wav to mono 16kHz float32 PCM using PyAV.
    """
    container = av.open(io.BytesIO(audio_bytes))
    stream = next(s for s in container.streams if s.type == "audio")
    resampler = av.audio.resampler.AudioResampler(format="s16", layout="mono", rate=16000)
    chunks = []
    for frame in container.decode(stream):
        for rf in resampler.resample(frame):
            chunks.append(rf.to_ndarray().reshape(-1))
    container.close()
    if not chunks:
        return np.zeros(0, dtype=np.float32)
    int16 = np.concatenate(chunks).astype(np.int16)
    return (int16.astype(np.float32) / 32768.0)

def transcribe_bytes(audio_bytes: bytes) -> str:
    """
    Transcribe bytes to text with VAD to remove silence.
    """
    audio = _decode_to_mono16k(audio_bytes)
    model = load_asr()
    segments, _ = model.transcribe(audio, vad_filter=True)
    return " ".join(seg.text.strip() for seg in segments)
