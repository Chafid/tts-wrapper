# TTS-Wrapper

*TTS-Wrapper* is a hassle-free Python library that allows one to use text-to-speech APIs with the same interface.

Currently the following services are supported:

- AWS Polly
- Google TTS
- Microsoft TTS

## Installation

Install using pip.

```
pip install TTS-Wrapper
```

## Usage

Simply instantiate an object from the desired service and call `synth()`.

```Python
from tts_wrapper import PollyTTS

tts = PollyTTS()
tts.synth('Hello, world!', 'hello.wav')
```

### Selecting a Voice

You can change the default voice by specifying the voice name and the language code:

```Python
tts = PollyTTS(voice_name='Camila', lang='pt-BR')
```

Check out the list of available voices for [Polly](https://docs.aws.amazon.com/polly/latest/dg/voicelist.html), [Google](https://cloud.google.com/text-to-speech/docs/voices), and [Microsoft](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices).

### SSML

You can also use [SSML](https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language) markup to control the output, like so:

```Python
tts.synth('Hello, <break time="3s"/> world!')
```

**You don't need to wrap it with the `<speak></speak>` tag as it is automatically used with the required parameters for each TTS service.**

Learn which tags are available for each service: [Polly](https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html), [Google](https://cloud.google.com/text-to-speech/docs/ssml), and [Microsoft](https://docs.microsoft.com/en-us/cortana/skills/speech-synthesis-markup-language).

### Credentials

You need to setup credentials to access each service.

#### Polly

If you don't explicitly define credentials, `boto3` will try to find them in your system's credentials file or your environment variables. However, you can specify them with:

```Python
from tts_wrapper import PollyTTS, AwsCredentials

tts = PollyTTS(creds=AwsCredentials('AWS_KEY_ID', 'AWS_ACCESS_KEY'))
```

#### Google

Point to your [Oauth 2.0 credentials file](https://developers.google.com/identity/protocols/OAuth2) path:

```Python
from tts_wrapper import GoogleTTS

tts = GoogleTTS(creds='path/to/creds.json')
```

#### Microsoft

Just provide your [subscription key](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#authentication), like so:

```Python
from tts_wrapper import MicrosoftTTS

tts = MicrosoftTTS(creds='TOKEN')
```