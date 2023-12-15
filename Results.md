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

Well, the much talked about Mixtral. I’m sure I’m not using the proper instruction format, so these results are going to be less than optimal, but let’s just spin it.

Query | Result
--- | ---
\"Sigismundo’s epopte is presented in IX:ll.15-28.\" | ... 