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
from spleeter.separator import Separator
from urllib.parse import urlparse
import os

app = FastAPI()
my_config = Config(
    region_name = 'us-west-2',
)
logger = logging.getLogger(__name__)

def extract_bucket_and_key(s3_uri):
    parsed_uri = urlparse(s3_uri)
    bucket_name = parsed_uri.netloc
    key = parsed_uri.path.lstrip('/')
    return bucket_name, key

def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method, Params=method_parameters, ExpiresIn=expires_in
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method
        )
        raise
    return url

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
    s3_client = boto3.client('s3', config=my_config)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        
    except ClientError as e:
        logging.error(e)
        return False
    return True

def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat="wav",
        LanguageCode="en-US",
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status in ["COMPLETED", "FAILED"]:
            print(f"Job {job_name} is {job_status}.")
            if job_status == "COMPLETED":
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}."
                )
                bucket, key = extract_bucket_and_key(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                presigned_url = generate_presigned_url(transcribe_client,"get_object",{"Bucket": bucket, "Key": key})
                return presigned_url
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)

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
    upload_file(filename+".mp3","karaoketranscribejob")
    transcribe_client = boto3.client("transcribe")
    file_uri = f's3://karaoketranscribejob/{filename+".mp3"}'
    transcribe_url = transcribe_file("Transcribed_job", file_uri, transcribe_client)
    return transcribe_url
    #ffmpeg.output(audio, filename+".mp3").run()

