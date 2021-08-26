import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

keys_file = open('Keys.json')
responses_file = open('Responses.json')

keys = json.load(keys_file)
responses = json.load(responses_file)

authenticator = IAMAuthenticator(keys['api-key'])
tone_analyzer = ToneAnalyzerV3(
    version=keys['version'],
    authenticator=authenticator
)
tone_analyzer.set_service_url(keys['url'])

text = "I hate you"

tone_analysis = tone_analyzer.tone(
    {"text": text},
    content_type="application/json"
).get_result()

tone_confidence = 0
most_likely_tone = None

for tone in tone_analysis["document_tone"]["tones"]:
    if tone_confidence < tone["score"]:
        most_likely_tone = tone
        tone_confidence = tone["score"]


print("Hmmmmmmmmm")
print("Im like")
print("{score}% sure that like".format(score=(float(most_likely_tone["score"])*100.0)))
print("ur being an {name}".format(name= responses[most_likely_tone["tone_id"]]))

keys_file.close()
responses_file.close()
