from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
import random
import string
import demucs.api
import os

app = FastAPI()
# Initialize with default parameters:
separator = demucs.api.Separator()

# Use another model and segment:
separator = demucs.api.Separator(model="mdx_extra")

import os
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/split_audio")
async def split_audio(source_audio: UploadFile):
    filename = "".join(random.choices(string.ascii_letters, k=8)) + ".mp3"
    with open(filename, "wb") as f:
        f.write(await source_audio.read())

    origin, separated = separator.separate_audio_file(filename)
    for file, sources in separated:
        for stem, source in sources.items():
            demucs.api.save_audio(source, f"{stem}_{file}", samplerate=separator.samplerate)
    #demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", filename, "-o", filename])

    os.rename(filename + "/mdx_extra/song/no_vocals.mp3", "static/" + filename)
    os.remove(filename)
    return "static/" + filename