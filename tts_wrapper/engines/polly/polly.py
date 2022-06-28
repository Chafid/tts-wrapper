from typing import Optional
from tts_wrapper.exceptions import UnsupportedFileFormat

from tts_wrapper.ssml import AbstractSSMLNode, SSMLNode

from ...tts import SSML, AbstractTTS, FileFormat
from . import PollyClient


class PollyTTS(AbstractTTS):
    def __init__(
        self,
        client: PollyClient,
        voice: Optional[str] = None,
    ) -> None:
        self.client = client
        self.voice = voice or "Joanna"

    def synth_to_bytes(self, ssml: SSML, format: FileFormat) -> bytes:
        if format != "wav":
            raise UnsupportedFileFormat(format, self.__class__.__name__)
        return self.client.synth(str(ssml), self.voice)

    def wrap_ssml(self, ssml: AbstractSSMLNode) -> AbstractSSMLNode:
        return SSMLNode.speak().add(ssml)
