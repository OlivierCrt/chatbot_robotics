from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from TTS.api import TTS
import tempfile
import os
import torch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

use_cuda = torch.cuda.is_available()
print(f"CUDA available: {use_cuda}")
if use_cuda:
    print("GPU:", torch.cuda.get_device_name(0))

print("Loading XTTS model...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=use_cuda)
print("XTTS loaded. Device:", "cuda" if use_cuda else "cpu")

SPEAKER_WAV = os.path.join(os.path.dirname(__file__), "voice.wav")

@app.get("/tts")
def tts_route(text: str = Query(...), lang: str = Query("fr")):
    fd, out_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)

    tts.tts_to_file(
        text=text,
        speaker_wav=SPEAKER_WAV,
        language=lang,
        file_path=out_path,
    )

    return FileResponse(out_path, media_type="audio/wav", filename="out.wav")

