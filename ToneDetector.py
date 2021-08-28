import json
from playsound import playsound
from ibm_watson import ToneAnalyzerV3, TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

keys_file = open('Keys.json')
responses_file = open('Responses.json')

keys = json.load(keys_file)
responses = json.load(responses_file)

authenticator = IAMAuthenticator(keys['tone-api-key'])
tone_analyzer = ToneAnalyzerV3(
    version=keys['tone-version'],
    authenticator=authenticator
)
tone_analyzer.set_service_url(keys['tone-url'])

text = input("What are you planning on saying? I'll tell you how you come across. You know you can tell me anything: ")

tone_analysis = tone_analyzer.tone(
    {"text": text},
    content_type="application/json"
).get_result()

tone_confidence = 0
most_likely_tone = None

if len(tone_analysis["document_tone"]["tones"]) == 0:
    voice_text = "What dog"
else:
    for tone in tone_analysis["document_tone"]["tones"]:
        if tone_confidence < tone["score"]:
            most_likely_tone = tone
            tone_confidence = tone["score"]
    voice_text = "Im like {score}% sure that like you're being an {name}".format(score=(float(most_likely_tone["score"])*100.0), name= responses[most_likely_tone["tone_id"]])

authenticator = IAMAuthenticator(keys['text-to-speech-api-key'])
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)
text_to_speech.set_service_url(keys['text-to-speech-url'])

with open('test.wav', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            voice_text,
            voice='en-US_AllisonV3Voice',
            accept='audio/wav'
        ).get_result().content)

playsound("test.wav")

keys_file.close()
responses_file.close()
