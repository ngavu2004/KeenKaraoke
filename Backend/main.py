from fastapi import FastAPI
import logging
import youtube_dl
import random
import string
import ffmpeg
import time
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from urllib.parse import urlparse
import os
import aiohttp
import asyncio
import io
import redis
import json
import requests


OPEN_AI_API_KEY = None
AWS_KEY_ID = None
AWS_KEY_SECRET = None

if None in [OPEN_AI_API_KEY, AWS_KEY_ID, AWS_KEY_SECRET]:
    raise Exception("One of the API Keys is missing")

app = FastAPI()
logger = logging.getLogger(__name__)
r = redis.Redis(host="localhost", port=6379, db=0)

s3_client = boto3.client(
    "s3",
    region_name="us-west-2",
    aws_access_key_id=AWS_KEY_ID,
    aws_secret_access_key=AWS_KEY_SECRET,
)


def extract_bucket_and_key(s3_uri):
    parsed_uri = urlparse(s3_uri)
    bucket_name = parsed_uri.netloc
    key = parsed_uri.path.lstrip("/")
    return bucket_name, key


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)

    except ClientError as e:
        logging.error(e)
        return False
    return True


@app.get("/fetch_audio")
async def fetch_audio(youtube_url: str):
    async with aiohttp.ClientSession() as sess:
        k = r.get(youtube_url)
        if k is None:
            filename = "".join(random.choices(string.ascii_letters, k=8)) + ".mp4"
            ydl_opts = {"format": "mp4", "verbose": True, "outtmpl": filename}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

            audio = ffmpeg.input(filename).audio
            ffmpeg.output(audio, filename + ".mp3").run()

            split_audio_json = None
            with open(filename + ".mp3", "rb") as f:
                split_audio_response = await sess.post(
                    "http://52.66.206.209:8000/split_audio",
                    data={"source_audio": f},
                    timeout=6000,
                )
                split_audio_json = await split_audio_response.json()
            # k = {"filename": filename, "split_audio_json": split_audio_json}
            # r.set(youtube_url, json.dumps(split_audio_json))
        else:
            k = json.loads(k)
            return k

        vocals_resp = requests.get(
            "http://52.66.206.209:8000/" + split_audio_json["vocals"]
        )
        with open("vocals.mp3", "wb") as f:
            f.write(vocals_resp.content)

        f_ = open("vocals.mp3", "rb")

        whisper_response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            files={
                "file": f_,
            },
            headers={"Authorization": "Bearer " + OPEN_AI_API_KEY},
            timeout=6000,
            data=[
                ("model", "whisper-1"),
                ("response_format", "verbose_json"),
                ("timestamp_granularities[]", "word"),
                ("timestamp_granularities[]", "segment"),
            ],
        )
        f_.close()
        resp = {
            "instrumentals": "http://52.66.206.209:8000/"
            + split_audio_json["no_vocals"],
            "transcription": whisper_response.json(),
        }
        r.set(youtube_url, json.dumps(resp))
        return resp
    # ffmpeg.output(audio, filename+".mp3").run()
