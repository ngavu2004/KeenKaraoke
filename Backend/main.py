from fastapi import FastAPI
import youtube_dl
import random
import string
import ffmpeg
from spleeter import separator

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

    prediction = separator.separate(audio)
    print(prediction)
    #ffmpeg.output(audio, filename+".mp3").run()