from google.cloud import speech, texttospeech, storage
import base64
import io
import os
import uuid

speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()
storage_client = storage.Client()

# Make sure to set this to your GCS bucket name
BUCKET_NAME = "fluent-long-audio"


def upload_blob(bucket_name, source_file_path, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Open the file in binary mode ('rb') for reading
    with open(source_file_path, "rb") as source_file:
        blob.upload_from_file(source_file)

    return f"gs://{bucket_name}/{destination_blob_name}"


def transcribe_audio(audio_file_path):
    """Transcribes audio from a file stored in Google Cloud Storage."""
    client = speech.SpeechClient()

    # Upload the audio to GCS
    gcs_uri = upload_blob(
        BUCKET_NAME, audio_file_path, os.path.basename(audio_file_path)
    )

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    try:
        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=90)

        if not response.results:
            return None

        transcript = response.results[0].alternatives[0].transcript

        # Clean up: delete the audio file from GCS
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(os.path.basename(audio_file_path))
        blob.delete()

        return transcript

    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None


def synthesize_text(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Journey-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    try:
        response = tts_client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return base64.b64encode(response.audio_content).decode("utf-8")
    except Exception as e:
        print(f"Text-to-speech error: {str(e)}")
        return None
