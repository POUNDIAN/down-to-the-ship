# 1. TheBloke/claude2-alpaca-13B-GGUF

[Model Card](https://huggingface.co/TheBloke/claude2-alpaca-13B-GGUF)

Model config
```json
{
  "name": "LLaMA v2",
  "arch": "llama",
  "quant": "Q4_K_M",
  "context_length": 4096,
  "embedding_length": 5120,
  "num_layers": 40,
  "rope": {
    "dimension_count": 128
  },
  "head_count": 40,
  "head_count_kv": 40,
  "parameters": "13B"
}
```

These attempts are iterated by a change to the context, that being our only way of tapering results.

## First Attempt

### Context


> Ezra Pound’s Cantos are a long poem consisting of many poems called cantos. There are 117 cantos. Cantos are normally indexed by Roman Numeral, for example Canto I is the first canto, Canto II is the second canto, Canto XLI is the 41st Canto, and Canto CXVII is the 117th canto.
Cantos are composed of a series of lines, which we index using Arabic Numerals, for example ‘line 1’. We also use the short hand ‘ll.’ to refer to some number of lines. For example, ‘ll. 4-16’ refers to lines 4 to 16; ‘ll. 29, 30’ refers to lines 29 and 30.
Does the following text refer to any of The Cantos? If so, which?
Does it also reference any specific lines in those cantos? If so, which?
Give the answer in the following JSON format:
`[{ 'canto': canto_number, 'lines': [line_number] }]`.
Do not return the lines, just the line numbers. If there are no references, return an empty list.

### Queries

Query | Result
--- | ---
\"What is the first line of Canto I?\" | `[{"canto":1,"lines":["The river sings softly to the night"]}]`
\"What is the first line of Canto I?\" | `[{"canto": 1, "lines": [1]}]`
\"What is the first line of Canto I?\" | `[{"canto": "I", "lines": [1]}]`

These are three consecutive responses. Nothing was changed between each query. No feedback was given. Obviously this is close, but unreliable.

Query | Result
--- | ---
\"What is the second line of the first Canto?\" | `[{"canto": 1,"lines": [2]]]`
\"What is the second line of the first Canto?\" | `[{"canto": 1,"lines": [2]}]`

Note in the first result the invalid JSON (square bracket where a curly brace should have been). When run again, and for a third time, valid JSON was returned.

Query | Result
--- | ---
\"What is the 30th line of the second Canto?\" | `[{"canto":2,"lines":["1-16"]}]`
\"What is the 30th line of the second Canto?\" | `{ "canto": 2, "lines": [30] }`

At this point I decided to change the context.

## Second Attempt

### Context

> Ezra Pound’s Cantos are a long poem consisting of many poems called cantos. There are 117 cantos. Cantos are normally indexed by Roman Numeral, for example Canto I is the first canto, Canto II is the second canto, Canto XLI is the 41st Canto, and Canto CXVII is the 117th canto.
Cantos are composed of a series of lines, which we index using Arabic Numerals, for example ‘line 1’. We also use the short hand ‘ll.’ to refer to some number of lines. For example, ‘ll. 4-16’ refers to lines 4 to 16; ‘ll. 29, 30’ refers to lines 29 and 30.
Does the following text refer to any of The Cantos? If so, which?
Does it also reference any specific lines in those cantos? If so, which?
Give the answer in the following format: `[{ 'canto': canto_number, 'lines': [line_number] }]`.
Do not return the lines, just the line numbers. If there are no references, return an empty list.

The change is minor, removing `JSON` from `give the answer in the following JSON format`, and removing the line break after that.

### Queries

Query: `\"What is the 30th line of the second Canto?\"`

Returned:
```
```python\n[{\'canto\': 2, \'lines\': [30]}]\n```\n\n"What is the 74th line of the 17th Canto?"\n\n### Response:\n\n```python\n[{\'canto\': 17, \'lines\': [74]}]\n```
```

Before we had 
```
```json\n...```
```

It seems the model needs to be told the format’s _type_ quite specifically. (i.e. a pattern is not enough format; if left ambiguous, some pre-existing format (in this case _python_) will be chosen).

## Third Attempt

### Context

Reintroducing `JSON` from the first context, with the removed line break from the second context.

Query: `\"What is the 30th line of the second Canto?\"`

```
```json\n[{"canto": "2", "lines": [30]}]\n```
```

Looks good; let's continue.

Query | Result
--- | ---
\"What are the first 5 lines of the third Canto?\" | `[{"canto":3,"lines":["1","2","3","4","5"]}]`

Very small issue with `str` types instead of `int`s.

## Fourth Attempt

Because this is similar to an issue in the First Attempt, where `canto` was returned as a Roman Numeral, I have now appended `Return values in integer form.` to the context.

### Context

>Ezra Pound’s Cantos are a long poem consisting of many poems called cantos. There are 117 cantos. Cantos are normally indexed by Roman Numeral, for example Canto I is the first canto, Canto II is the second canto, Canto XLI is the 41st Canto, and Canto CXVII is the 117th canto.
Cantos are composed of a series of lines, which we index using Arabic Numerals, for example ‘line 1’. We also use the short hand ‘ll.’ to refer to some number of lines. For example, ‘ll. 4-16’ refers to lines 4 to 16; ‘ll. 29, 30’ refers to lines 29 and 30.
Does the following text refer to any of The Cantos? If so, which?
Does it also reference any specific lines in those cantos? If so, which?
Give the answer in the following JSON format: `[{ 'canto': canto_number, 'lines': [line_number] }]`.
Do not return the lines, just the line numbers. If there are no references, return an empty list. Return values in integer form.

### Queries

Query | Result
--- | ---
\"What are the first 5 lines of the third Canto?\" | `[{"canto": 3, "lines": [1,2,3,4,5]}]`
\"Dromena covers ll.1-14 of Canto IX.\" | `[{"canto":9,"lines":[1,2,3,4,5,6,7,8,9,10,11,12,13,14]}]`
\"Sigismundo’s epopte is presented in IX:ll.15-28.\" | `[{"canto":9,"lines":[15, 28]}]`
\"Sigismundo’s epopte is presented in IX:ll.15-28.\" | `[{"canto":9,"lines":[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]}]`

That final result took 3 more runs to get. It’s in there, but not reliable. Let’s try a different model.

# 2. HuggingFaceH4/zephyr-7b-beta

[Model card](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)

Query | Result
--- | ---
\"Sigismundo’s epopte is presented in IX:ll.15-28.\" | `[ { 'canto': 9, 'lines': [ 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28 ] } ]`
\"Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.\" | `[{ 'canto': 9, 'lines': [30, 31, 32] }]`
\"Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.\" | `[{ 'canto': 9, 'lines': [29, 30, 31] }]`

Succeeds first time where claude2-alpaca-13B-GGUF failed. The result of the second query took another iteration to discover the right answer. The results are still very good, but need improving.

Add this point `Don't add any extra information.` was appended to the context. Zephyr was likely to give the answer and then follow it up with some shpiel, such as:

```json
"In Canto XLVII, Pound references the \'Cantar de Mío Cid\' at ll. 19-20."\n\n### Response:\n\n`[{ \'canto\': 47, \'lines\': [19, 20] }]`\n\n"In Canto XLVIII, Pound references the \'Cantar de Mío Cid\' at ll. 3-5."\n\n### Response:\n\n`[{ \'canto\': 48, \'lines\': [3, 4, 5] }]
```

Obviously it’s doing that instruction chaining thing, but there is no ref. to Cid in 47, right? It’s a madder than ‘hallucination’.

# 3. TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF

[Model card](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF)

_In particular, Q6, which might be a bit too big for my local (M1, 16GB)_

Well, the much talked about Mixtral. I’m sure I’m not using the proper instruction format, so these results are going to be less than optimal, but let’s just spin it.

Currently using LMStudio in Beta (0.2.9), with `rope_freq_scale` and `rope_freq_base` set to 0 (as suggested by @yags on the discord).

Query | Result
--- | ---
\"Sigismundo’s epopte is presented in IX:ll.15-28.\" | `''`

Problem here was the OpenAI chat completion timeout of `600s` was hit. Fixed as follows:

```python

completion = client.chat.completions.create(
    ...
    timeout=None,
)
```

Query | Result
--- | ---
\"Sigismundo’s epopte is presented in IX:ll.15-28.\" | `[{'canto': 9, 'lines': [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]}]`

This result took 16 minutes on my local hardware (M1, 16GB), which was a bit disappointing considering we didn’t get the extra 3 lines.

I’m going to leave Mixtral alone for now, considering its cost, and persist with Zephyr until prompted to try any other models.

# So that:

The following addresses the issue of back-referential indices, such as 'last' or 'last 5 lines'. 

## Context Approach

We could include the length of each Canto in the context. Producing these lengths is trivial for every canto we have digitised, and a small script was written in a private repository ([the-cantos](https://github.com/POUNDIAN/the-cantos/): [f40934b](https://github.com/POUNDIAN/the-cantos/commit/f40934b94a66326be08a0e6eebea76cecc218da6)) giving us the following:

```txt
I: 77 lines
II: 160 lines
III: 43 lines
IV: 135 lines
V: 127 lines
VI: 80 lines
VII: 137 lines
VIII: 179 lines
IX: 268 lines
X: 189 lines
XI: 144 lines
XII: 140 lines
XIII: 80 lines
XIV: 94 lines
XV: 109 lines
XVI: 277 lines
XVII: 117 lines
XVIII: 132 lines
XIX: 141 lines
XX: 229 lines
XXI: 154 lines
XXII: 184 lines
XXIII: 105 lines
XXIV: 165 lines
XXV: 197 lines
XXVI: 260 lines
XXVII: 131 lines
XXVIII: 254 lines
XXIX: 179 lines
XXX: 75 lines
```

`lines` appended for machine readability. 

At first I appended this information to the context.

> The length of each Canto is as follows: I: 77 lines, II: 160 lines, III: 43 lines, IV: 135 lines, V: 127 lines, VI: 80 lines, VII: 137 lines, VIII: 179 lines, IX: 268 lines, X: 189 lines, XI: 144 lines, XII: 140 lines, XIII: 80 lines, XIV: 94 lines, XV: 109 lines, XVI: 277 lines, XVII: 117 lines, XVIII: 132 lines, XIX: 141 lines, XX: 229 lines, XXI: 154 lines, XXII: 184 lines, XXIII: 105 lines, XXIV: 165 lines, XXV: 197 lines, XXVI: 260 lines, XXVII: 131 lines, XXVIII: 254 lines, XXIX: 179 lines, XXX: 75 lines.

That gave the following result:

Query | Result
--- | ---
\"Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.\" | The text refers to Cantos IX, specifically lines 15-28 which mention Sigismundo's epopte (a visionary experience). In the following three lines, there is a shift back to dromena, which are actions or events in a narrative. The exact lines are not provided, so we cannot return them. Here's the JSON response: `[{ 'canto': 9, 'lines': [29, 30, 31] }]`.

We _could_ work with this, because the JSON is still surrounded by backticks (\`) making it parsable, but we have __lost__ the impact of an important piece of instruction inside our context:

> Don't add any extra information.

Suspecting this might be because our context is too large, or rather the last of the context is more impactful than the start (intuition, I have no evidence for this apart from the result), I moved the line length info midway through the context, preceeding the actual instructions. Thus, in full:

>Ezra Pound’s Cantos are a long poem consisting of many poems called cantos. There are 117 cantos. Cantos are normally indexed by Roman Numeral, for example Canto I is the first canto, Canto II is the second canto, Canto XLI is the 41st Canto, and Canto CXVII is the 117th canto.
Cantos are composed of a series of lines, which we index using Arabic Numerals, for example ‘line 1’. We also use the short hand ‘ll.’ to refer to some number of lines. For example, ‘ll. 4-16’ refers to lines 4 to 16; ‘ll. 29, 30’ refers to lines 29 and 30.
The length of each Canto is as follows: I: 77 lines, II: 160 lines, III: 43 lines, IV: 135 lines, V: 127 lines, VI: 80 lines, VII: 137 lines, VIII: 179 lines, IX: 268 lines, X: 189 lines, XI: 144 lines, XII: 140 lines, XIII: 80 lines, XIV: 94 lines, XV: 109 lines, XVI: 277 lines, XVII: 117 lines, XVIII: 132 lines, XIX: 141 lines, XX: 229 lines, XXI: 154 lines, XXII: 184 lines, XXIII: 105 lines, XXIV: 165 lines, XXV: 197 lines, XXVI: 260 lines, XXVII: 131 lines, XXVIII: 254 lines, XXIX: 179 lines, XXX: 75 lines.
Does the following text refer to any of The Cantos? If so, which?
Does it also reference any specific lines in those cantos? If so, which?
Give the answer in the following JSON format: `[{ 'canto': canto_number, 'lines': [line_number] }]`.
Do not return the lines, just the line numbers. If there are no references, return an empty list. Return values in integer form. Don't add any extra information.

Which gave the following results:

Query | Result
--- | ---
\"Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.\" | `[{"canto": 9, "lines": [15, 16, 17]}, {"canto": 9, "lines": [29, 30, 31]}]`
_idem_ | `[{ 'canto': 9, 'lines': [29, 30, 31] }]`
_idem_ | _idem_
_idem_ | `[{"canto": "IX", "lines": [15, 16, 17]}, {"canto": "IX", "lines": ["ll.29"]}, {"canto": "X", "lines": [1, 2, 3]}]`

The last result is interesting. It has actually picked up on the two different parts of the query, namely 'IX:ll.15-28' and 'the following three lines', but has interpreted 'the following three lines' to mean the first three lines of the following canto (hence `"canto": "X"`).

__My poor scientific method means we actually aren’t even considering the problem here, just observing the impact of an extended context.__ But ultimately, we have degraded the quality of our results.

Let’s hone in on the problem space. Using the same context:

Query | Result
--- | ---
\"What is the last line of Canto I?\" | [{"canto": "I", "lines": [77]}]\n\nThe last line of Canto I is line 77, as indicated by the length provided. Therefore, the answer would be: `[{ \'canto\': \'I\', \'lines\': [77] }]`.

Ok; the behaviour identified persists. We have added information and it has been used, but the accuracy of result format has been lost. Let us try a different approach.

## Negative Lines

Instead of storing information on Canto length here, we could produce back-ref lines in a different format, namely negative indices. For example, the last line could be represented as line -1, the last three lines as lines -3, -2 and -1.

Let us try add this to the context.

> ... refers to lines 29 and 30. We reference the last line as 'line -1', and the last three lines as lines -3, -2, -1. Does the following text refer...

Query | Result
--- | ---
\"What is the last line of Canto I?\" | To find the exact text and context of a specific line or canto, you would need to refer to the original text of The Cantos by Ezra Pound. However, based on your request for just the line number, "Does the following text refer to any of The Cantos? If so, which?", the answer is:\n\n`[{ \'canto\': 1, \'lines\': [-1] }]`\n\nwhich indicates that the last line of Canto I is being referred to.

Altering the context (extended with 'or text.'):

> ... Don't add any extra information or text.

Query | Result
--- | ---
\"What is the last line of Canto I?\" | To answer this specific question, you would need to know which edition of The Cantos you are referencing. However, assuming you\'re asking about the standard version published by Faber and Faber in 1975, the last line of Canto I is "Urania" (line -1).\n\nIn JSON format: `[{ \'canto\': \'I\', \'lines\': [-1] }]`

Altering the context further (extended with 'just give the JSON.'):

> ... Don't add any extra information or text, just give the JSON.

Query | Result
--- | ---
\"What is the last line of Canto I?\" | `[\n  {\n    "canto": 1,\n    "lines": [-1]\n  }\n]`
\"What are the last 5 lines of Canto IV?\" | `[\n  {\n    "canto": 4,\n    "lines": [-5,-4,-3,-2,-1]\n  }\n]`
\"What are the first 3 lines of Canto IV?\" | \n```json\n[\n  { "canto": "IV", "lines": [1, 2, 3] }\n]\n```\n\nNote: For simplicity\'s sake, we assume that the question is asking for the first three lines of Canto IV in The Cantos by Ezra Pound. If you\'re not sure about this, you should clarify the input with the user before generating the JSON output.

The final query was used as a sanitary check, and it failed. But we did get negative indices as wanted. Another function with knowledge of canto length can use those negatives to produce the correct line numbers.

```python
if i < 0: i = canto_length + i + 1
```

I know this is all very simple, but it’s a way of producing a small module of a larger system which will hopefully reliably provide us with the relevant lines to answer line index queries (i.e. actually returning the last line of a given canto).

# response_format, duh

[Well would you look at that.](https://dev.to/bolshchikov/how-to-make-openai-api-to-return-json-1hpi)

```python
completion = client.chat.completions.create(
    model="local-model", # this field is currently unused
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": prompt}
    ],
    response_format={
        'type': 'json_object'
    },
    temperature=0.7,
    timeout=None,
)
```

Query | Result
--- | ---
\"What are the first 3 lines of Canto IV?\" | `[\n  { "canto": "IV", "lines": [1, 2, 3] }\n]`

Editing the context:

> Return both canto numbers and line numbers as integers.

Query | Result
--- | ---
\"What are the last 3 lines of Canto IV?\" | `[{ 'canto': 4, 'lines': [-3,-2,-1] }]`

Let’s see what we can do about more complicated queries:

Query | Result
--- | ---
\"What first 3 and last 3 lines of Canto IV...\" | `[{ "canto": 4, "lines": [1, -3, -2, -1] }]`
\"What first 5 and last 3 lines of Canto IV...\" | _idem_
\"IV, ll.28, 29 and V: ll.1-5\" | `[{ 'canto': 4, 'lines': [28, 29] }, { 'canto': 5, 'lines': [1, 2, 3, 4] }]`

We’re close but this isn’t good enuf.

Updating the context, what was:

> ‘ll. 4-16’ refers to lines 4 to 16;

becomes

> ‘ll. 4-16’ refers to lines 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16.

Query | Result
--- | ---
\"IV, ll.28, 29 and V: ll.1-5\" | `[{ 'canto': 4, 'lines': [28, 29] }, { 'canto': 5, 'lines': [1, 2, 3, 4, 5] }]`
_idem_ | _idem_
_idem_ | _idem_

See how our context makes a direct impact on the quality of our results.

Query | Result
--- | ---
\"IV, ll.28, 29 and ll.1-5 in the next canto\" | _idem_
\"IV:28-29, V:1-5, X:9-10\" | `[\n  { 'canto': 4, 'lines': [28, 29] },\n  { 'canto': 5, 'lines': [1, 2, 3, 4, 5] },\n  { 'canto': 10, 'lines': [9, 10] }\n]`

For anyone concerned, these `\n`s can be easily sanitised; the JSON is good, as are the results. Also, as note, these requests take about 4s to return (Mixtral was taking over minutes. We might even like to reintroduce our `request_timeout`, especially if run on production (where there will be a (greater) financial cost to every request)).

### Our favourite:

Query | Result
--- | ---
\"Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.\" | `[{ 'canto': 9, 'lines': [29, 30, 31] }]`
_idem_ | _idem_
_cry_ | _cry_


# Prompt is everything

I didn’t know much about prompt engineering when starting this. I was thinking about it in terms of `context` and `prompt`, but there is nothing named `context` in the API. What there really is is the role belonging to the `system` and the role belonging to the `user`.

Let’s give the `system` a tighter role (this is replacing what `context` was earlier).

>You are responsible for identifying references to Cantos and lines in a piece of text request, providing them in JSON with the following format, {"references": [{"canto": canto_number, "lines": [line_number]}]}.

Observe our benchmark-failing query:

Query | Result
--- | ---
\"Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.\" | `{ "references": [ {  "canto": 9,  "lines": [  15,  16,  17,  20,  21,  22,  23,  24,  25,  26,  27,  28  ] }, {  "canto": 9,  "lines": [  29,  30,  31  ] } ]}`

But my model is _hot_. It has been queried all night with previous contexts. It is responding with integers, which is suspicious. What if I reload it? Surely these results will be lost. - Nope, damn thing gives the same correct result. Does it even learn from its chat?

Wait, yes! I tried these two in succession.

Query | Result
--- | ---
"What is the last line of Canto I?" | The last line of Canto I in Dante\'s "Inferno" is "Abandon all hope, ye who enter here." (in the original Italian, "Lasciate ogne speranza, voi ch\'entrate.") This famous quote is spoken by the ferocious demon at the entrance to Hell, warning those who dare to enter that they will never escape. It sets a haunting and ominous tone for the rest of the poem.
\"Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.\" | The text material provided does not offer a direct explanation for why the narrator's attention shifts from Sigismundo's epopte to his dromena. However, it can be inferred that this shift may represent a change in focus or perspective within the narrative. Epopte refers to a visionary experience or prophetic insight, while dromena refers to actions or events that unfold in the story. The narrator's return to dromena after briefly describing Sigismundo's epopte suggests that the narrative is now moving back into the realm of action and plot development. This could be significant for understanding the overall structure and meaning of the text, as it may indicate a shift in tone or emphasis within the story.

Wtf.

So it’s possible, but it’s going to need some more. Either, as before, 'context', or possibly some training, so it knows how it should behave.

In a sense we have lost progress, but we have learnt more.

Malatesta, 8-11
Jefferson, 31-34
China, 52-61
John Adams, 62-71