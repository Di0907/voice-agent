import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Force CPU & disable cuDNN
os.environ["CUDA_VISIBLE_DEVICES"] = ""
torch.backends.cudnn.enabled = False

# Choose a small model (quality vs speed)
MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
# MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # even faster on CPU

_tok = None
_model = None
_pipe = None

def load_llm(model_id: str = MODEL_ID, max_new_tokens: int = 96, temperature: float = 0.6):
    """
    Load instruction-tuned LM on CPU and return a text-generation pipeline.
    """
    global _tok, _model, _pipe
    if _pipe is None:
        _tok = AutoTokenizer.from_pretrained(model_id)
        _model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            device_map="cpu",
        )
        _pipe = pipeline(
            task="text-generation",
            model=_model,
            tokenizer=_tok,
            max_new_tokens=max_new_tokens,  # shorter for faster first response
            do_sample=True,
            temperature=temperature,
        )
    return _pipe

SYS_PROMPT = "You are a helpful voice assistant. Keep your answers short and clear."

def chat_reply(history):
    """
    history: list of {"role": "user"/"assistant", "content": "..."}
    """
    sys = f"System: {SYS_PROMPT}"
    lines = [sys] + [f"{m['role'].capitalize()}: {m['content']}" for m in history] + ["Assistant:"]
    prompt = "\n".join(lines)
    pipe = load_llm()
    out = pipe(prompt)[0]["generated_text"]
    return out.split("Assistant:")[-1].strip()
