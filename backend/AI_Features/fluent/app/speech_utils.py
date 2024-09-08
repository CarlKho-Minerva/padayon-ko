from google.cloud import speech, texttospeech
import base64
import io

speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()


def transcribe_audio(audio_content):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code="en-US",
        # Add max_alternatives to get multiple transcription options
        max_alternatives=1,
        # Enable automatic punctuation
        enable_automatic_punctuation=True,
    )

    try:
        # Use long_running_recognize for longer audio files
        operation = speech_client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=90)  # Increased timeout to 90 seconds

        if not response.results:
            return None

        return response.results[0].alternatives[0].transcript
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
        audio_encoding=texttospeech.AudioEncoding.MP3  # Changed to MP3 for better compatibility
    )

    try:
        response = tts_client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return base64.b64encode(response.audio_content).decode("utf-8")
    except Exception as e:
        print(f"Text-to-speech error: {str(e)}")
        return None
