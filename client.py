from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:1234/v1',
    api_key='not_needed'
)

context = """Ezra Pound’s Cantos are a long poem consisting of many poems called
cantos. There are 117 cantos. Cantos are normally indexed by Roman Numeral,
for example Canto I is the first canto, Canto II is the second canto, Canto XLI
is the 41st Canto, and Canto CXVII is the 117th canto.
Cantos are composed of a series of lines, which we index using Arabic Numerals,
for example ‘line 1’. We also use the short hand ‘ll.’ to refer to some number
of lines. For example, ‘ll. 4-16’ refers to lines 4 to 16; ‘ll. 29, 30’ refers
to lines 29 and 30.
Does the following text refer to any of The Cantos? If so, which?
Does it also reference any specific lines in those cantos? If so, which?
Give the answer in the following JSON format: `[{canto: [line]}]`.
"""

prompt = """
\"What is the first line of Canto I?\"
"""

completion = client.chat.completions.create(
    model="local-model", # this field is currently unused
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
)

print(completion.choices[0].message)