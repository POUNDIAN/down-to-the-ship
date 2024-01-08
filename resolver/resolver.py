import json
import requests

CANTOS_URL = 'http://localhost:9001/2015-03-31/functions/function/invocations'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}


def resolve_references(references):
    data = { 'body': { 'references': references } }
    response = requests.get(CANTOS_URL, headers=headers, data=json.dumps(data))
    text = response.text.encode().decode('unicode-escape')
    text = json.loads(text)
    return text


example_references = [
        {
            "canto": "I",
            "lines": [4, 5, 6]
        },
        {
            "canto": "IV",
            "lines": [-1]
        }
    ]

print(resolve_references(example_references))

# Output:
# [{'canto': 'I', 'lines': [{'number': 1, 'content': 'And then went down to the ship,'}, {'number': 2, 'content': 'Set keel to breakers, forth on the godly sea, and'}, {'number': 3, 'content': 'We set up mast and sail on that swart ship,'}]}, {'canto': 'IV', 'lines': [{'number': -1, 'content': '         there in the arena...'}]}]