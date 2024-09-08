from google.cloud import speech, texttospeech
import base64

speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()


from google.cloud import speech, texttospeech
import base64

speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()


def transcribe_audio(audio_content):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    try:
        response = speech_client.recognize(config=config, audio=audio)

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
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    response = tts_client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    return base64.b64encode(response.audio_content).decode("utf-8")
