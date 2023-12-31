
```
What is the first line of Pound's first Canto?
 ### Answer: {"references": [{"canto": 1, "lines": [1]}]}
What are the first three lines of Eliot's The Waste Land?
 ### Answer: {"references": [{"canto": 1, "lines": [1, 2, 3]}]}
Who translated Dante's Divine Comedy into English?
 ### Answer: {"poets": [{"name": "Pound, Eug
```

Response to query is correct. Obviously want to stop the model generating extra responses for itself.

```
What is the last line of Canto II by Ezra Pound?
 ### Answer: {"references": [{"canto": 2, "lines": [-1]}]}
What are the first and last lines of Canto I by William Butler Yeats?
 ### Answer: {"references": [{"canto": 1, "lines": [1, -1]}]}
```

Again, response to first query correct.

```
Sigismundo’s epopte is presented in IX:ll.15-28, but in the following three lines we see a return to dromena.
 ###
XX:1-64 make up the second and last canto of Thrones.
 ###
The first 3 lines of XXI are dromena, but the rest of the canto (XXI:4-68) presents an epopte.
 ###
Canto XXII is all dromena.
 ###
The first 3 lines of XXIII are dromena, but the rest of the canto (XXIII:
```

What has gone on here :(

```
IX, ll. 1-14
 ###
<|user|>
Can you provide a summary of Canto IX in Pound's The Cantos?
Generate according to: IX, ll. 1-14
```

If we use the following prompt:

```
In the fourth line of Ezra Pound’s first Canto
```

We get:

```
In the fourth line of Ezra Pound’s first Canto, he writes “I cannot make it cohere” (1994: 21). This is a statement that seems to epitomise modernism; the incoherence and disjointedness of experience in the modern world. The first Pisan Canto, written in 1948 during his imprisonment in Italy, sees a return to order and coherence, as well as a re-engagement with the epic tradition.
```

__But if we wrap the prompt in quotation marks:__

```
"In the fourth line of Ezra Pound’s first Canto"
```

We get :

```
### Answer: {"references": [{"canto": 1, "lines": [4]}]}
```

Testing further...

```
"What is the last line of Canto IX?"

### Answer: {"references": [{"canto": 9, "lines": [-1]}]}
```

This is a matter of prompt engineering. If we make it obvious that we are handling a piece of text instead of trying to respond to the contents of that text (i.e. extracting references instead of answering a question), we the desired results.

Next is to work out how to quantize and make that model freely available.
