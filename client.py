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

response_context = """Ezra Pound’s Cantos are a long poem consisting of many poems called cantos. There are 117 cantos. Cantos are normally indexed by Roman Numeral, for example Canto I is the first canto, Canto II is the second canto, Canto XLI is the 41st Canto, and Canto CXVII is the 117th canto.
Here are a few lines you might find useful in answering the following question.
"""

# prompt = """
# \"Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.\"
# """

async def query(prompt, context=None, json=False):
    context = reference_context
    if context:
        context = response_context + '\n' + context
    
    response_format = None
    if json:
        response_format={
            'type': 'json_object'
        },

    completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ],
        response_format=response_format,
        temperature=0.0,
        timeout=None,
    )

    return completion.choices[0].message.content