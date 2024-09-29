from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
import random
import string
import demucs.separate
import os
from time import sleep

app = FastAPI()
# Initialize with default parameters:
#separator = demucs.api.Separator()

# Use another model and segment:
#separator = demucs.api.Separator(model="mdx_extra")

import os
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/split_audio")
async def split_audio(source_audio: UploadFile):
    random_string = "".join(random.choices(string.ascii_letters, k=8))
    filename = random_string+".mp3"
    with open(filename, "wb") as f:
        f.write(await source_audio.read())

    #origin, separated = separator.separate_audio_file(filename)
    #for file, sources in separated:
    #    for stem, source in sources.items():
    #        demucs.api.save_audio(source, f"{stem}_{file}", samplerate=separator.samplerate)
    demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", filename, "-o", filename + "_out"])
    while True:
        try:
            sleep(10)
            no_vocals_filename = "static/" + random_string + "_no_vocals.mp3"
            vocals_filename = "static/" + random_string + "_vocals.mp3"
            os.rename(filename + f"_out/mdx_extra/{random_string}/no_vocals.mp3", no_vocals_filename)
            os.rename(filename + f"_out/mdx_extra/{random_string}/vocals.mp3", vocals_filename)
            os.remove(filename)
        except Exception as e:
            print(".", endl="")
            continue
        break
    return {
        "no_vocals": no_vocals_filename,
        "vocals": vocals_filename,
    }