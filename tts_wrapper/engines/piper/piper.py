from typing import Any, List, Optional, Dict

from tts_wrapper.exceptions import UnsupportedFileFormat

from ...tts import AbstractTTS, FileFormat
from . import PiperClient, PiperSSML
import threading
import time

class PiperTTS(AbstractTTS):
    @classmethod
    def supported_formats(cls) -> List[FileFormat]:
        return ["wav", "mp3"]

    def __init__(self, client: PiperClient, lang: Optional[str] = None, voice: Optional[str] = None):
        super().__init__()  # This is crucial
        self._client = client
        self._voices = self.get_voices()
        self.set_voice(voice or "Joanna", lang or "en-US")
        self.audio_rate = 16000

    def synth_to_bytes(self, text: Any, format: Optional[FileFormat] = "wav") -> bytes:
        if format not in self.supported_formats():
            raise UnsupportedFileFormat(format, self.__class__.__name__)
        word_timings = self._client.get_speech_marks(str(text), self._voice)
        self.set_timings(word_timings)
        return self._client.synth(str(text), self._voice, format)

    @property
    def ssml(self) -> PiperSSML:
        return PiperSSML()

    def get_voices(self) -> List[Dict[str, Any]]:
        """Retrieves a list of available voices from the Polly service."""
        return self._client.get_voices()
                
    def set_voice(self, voice_id: str, lang_id: str):
        """
        Sets the voice for the TTS engine and updates the SSML configuration accordingly.
        Note that piper uses a model name - not voice details but we will abstract this so you can. 
        It will look through the list of self._voices and find the model file that matches the name and lang code
        

        @param voice_id: The ID of the voice to be used for synthesis.
        """

        super().set_voice(voice_id)  # Optionally manage voice at the AbstractTTS level if needed
        self._voice = voice_id
        self._lang = lang_id
