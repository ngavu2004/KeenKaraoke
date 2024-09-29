from fastapi import FastAPI
import youtube_dl
import random
import string
import ffmpeg
from spleeter.separator import Separator

app = FastAPI()

@app.get("/fetch_audio")
async def fetch_audio(youtube_url: str):
    filename = "".join(random.choices(string.ascii_letters, k=8)) + ".mp4"
    ydl_opts = {
        "format": "mp4",
        "verbose": True,
        "outtmpl": filename
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    audio = ffmpeg.input(filename).audio
    ffmpeg.output(audio, filename+".mp3").run()

    separator = Separator("spleeter:2stems")
    separator.separate_to_file(filename+".mp3", 'test')
    #ffmpeg.output(audio, filename+".mp3").run()