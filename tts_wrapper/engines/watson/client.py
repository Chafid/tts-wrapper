from typing import Tuple, List, Dict, Any

from ...exceptions import ModuleNotInstalled

try:
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator  # type: ignore
    from ibm_watson import TextToSpeechV1  # type: ignore
except ImportError:
    IAMAuthenticator = None
    TextToSpeechV1 = None

Credentials = Tuple[str, str]

FORMATS = {"wav": "audio/wav", "mp3": "audio/mp3"}


class WatsonClient:
    def __init__(self, credentials: Credentials) -> None:
        if IAMAuthenticator is None or TextToSpeechV1 is None:
            raise ModuleNotInstalled("ibm-watson")

        api_key, api_url = credentials
        client = TextToSpeechV1(authenticator=IAMAuthenticator(api_key))
        client.set_service_url(api_url)
        self._client = client

    def synth(self, ssml: str, voice: str, format: str) -> bytes:
        return (
            self._client.synthesize(text=str(ssml), voice=voice, accept=FORMATS[format])
            .get_result()
            .content
        )

    def get_voices(self) -> List[Dict[str, Any]]:
        """Fetches available voices from IBM Watson TTS service."""
        voice_data = self._client.list_voices().get_result()
        voices = voice_data["voices"]
        standardized_voices = []
        for voice in voices:
            standardized_voice = {}
            standardized_voice['id'] = voice['name']
            standardized_voice['language_codes'] = [voice['language']]
            standardized_voice['display_name'] = voice['name'].split('_')[1].replace('V3Voice', '')
            standardized_voice['gender'] = voice['gender']
            standardized_voices.append(standardized_voice)
        return standardized_voices
    