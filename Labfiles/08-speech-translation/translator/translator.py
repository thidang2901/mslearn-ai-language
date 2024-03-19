import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv
from playsound import playsound


def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('fr')
        translation_config.add_target_language('es')
        translation_config.add_target_language('hi')
        print('Ready to translate from', translation_config.speech_recognition_language)

        # Configure speech
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)

        # Get user input
        target_language = ''
        while target_language != 'quit':
            target_language = input(
                '\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n').lower()
            if target_language in translation_config.target_languages:
                translate(target_language)
            else:
                target_language = 'quit'

    except Exception as ex:
        print(ex)


def translate(target_language):
    # Translate speech
    # audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    # translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)
    # print("Speak now...")
    # result = translator.recognize_once_async().get()
    # print('Translating "{}"'.format(result.text))
    # translation = result.translations[targetLanguage]
    # print(translation)
    audio_file = 'station.wav'
    playsound(audio_file)
    audio_config = speech_sdk.AudioConfig(filename=audio_file)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)
    print("Getting speech from file...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[target_language]
    print(translation)

    # Synthesize translation
    voices = {
        "fr": "fr-FR-HenriNeural",
        "es": "es-ES-ElviraNeural",
        "hi": "hi-IN-MadhurNeural"
    }
    speech_config.speech_synthesis_voice_name = voices.get(target_language)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)


if __name__ == "__main__":
    main()
