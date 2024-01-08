## Resolving references

I have a repo, [cantos](https://github.com/POUNDIAN/cantos/), which not only stores whatever Cantos I have digitised, but also contains a small API (which can be run locally or on AWS) that takes JSON objects stating a number of references, i.e.

```json
[
    {
        "canto": "I",
        "lines": [4, 5, 6]
    },
]
```

and populates the object with the lines, returning this:

```json
{
    "canto": "I",
    "lines": [
        {"number": 4, "content": "Bore sheep aboard her, and our bodies also"},
        {"number": 5, "content": "Heavy with weeping, and winds from sternward"},
        {"number": 6, "content": "Bore us out onward with bellying canvas,"}
    ]
}
```

Using this result, we would extend the context to the query to our model and run the actual query (as opposed to our first stage, asking what references are contained in the query).
