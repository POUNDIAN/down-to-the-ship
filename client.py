from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:1234/v1',
    api_key='not_needed'
)

reference_context = """Ezra Pound’s Cantos are a long poem consisting of many poems called cantos. There are 117 cantos. Cantos are normally indexed by Roman Numeral, for example Canto I is the first canto, Canto II is the second canto, Canto XLI is the 41st Canto, and Canto CXVII is the 117th canto.
Cantos are composed of a series of lines, which we index using Arabic Numerals, for example ‘line 1’. We also use the short hand ‘ll.’ to refer to some number of lines. For example, ‘ll. 4-16’ refers to lines 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16. ‘ll. 29, 30’ refers to lines 29 and 30.
We reference the last line as 'line -1', and the last three lines as lines -3, -2, -1.
Does the following text refer to any of The Cantos? If so, which?
Does it also reference any specific lines in those cantos? If so, which?
Give the answer in the following JSON format: `[{ 'canto': canto_number, 'lines': [line_number] }]`.
Do not return the lines, just the line numbers. If there are no references, return an empty list. Return both canto numbers and line numbers as integers. You must return the JSON as a string, and nothing else. There should be no part of your response that is not the JSON object.
"""

context = """You are responsible for identifying references to Cantos and lines in a piece of text. Extract the references and return them as a single JSON object in the format {"references": [{"canto": canto_number, "lines": [line_number]}]}. Return only the JSON.
"""

prompt = """
\"Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.\"
"""

# prompt = "What is the last line of Canto I?"

completion = client.chat.completions.create(
    model="local-model", # this field is currently unused
    messages=[
        {"role": "system", "content": reference_context},
        {"role": "user", "content": prompt}
    ],
    response_format={
        'type': 'json_object'
    },
    temperature=0.0,
    timeout=None,
)

print(completion.choices[0].message)