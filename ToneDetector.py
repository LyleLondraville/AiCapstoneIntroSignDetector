import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

keys_file = open('Keys.json')
keys = json.load(keys_file)

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

print(json.dumps(tone_analysis, indent=2))

keys_file.close()
