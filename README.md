# down to the ship

Experiment write-up: [POUNDIAN / down-to-the-ship](https://poundian.com/experiments/down-to-the-ship)

View `deploy` for instructions on running the model.

## Guide

Three things went on in this experiment.

1. Testing base models locally, using LMStudio, experimenting with prompt engineering to try get the best results. This is kept in `./research`

2. Fine-tuning our best performing model (Zephyr 7B β) to behave from cold (cf. the results of part 1). This is detailed in `./train`

3. A failed attempt to merge the base model with our fine-tuned adapters. This is kept in `./merge`

4. Establishing a way of deploying and using the model with a bit of longevitity. At the moment we have to run the model on a GPU, which for me means using a [brev.dev](https://brev.dev) instance. This is kept in `./deploy`

## Intent

We wanted to be able to reliably return very simple queries about The Cantos, mainly 'lookup'.

LLMs currently offer little success. They are actually quite good at the flagship 'And then went...', but when asked for the second line, or the third, or the last, or a line from another Canto, they fail.

That is such a simple piece of functionality that I thought it good to solve it straightaway. What results is a system that extracts references to lines. To complete this project we would need to do two things:

1. Take those references and return the lines.

2. Take those lines, put them in the 'context', and pass both the initial query and context to another LLM for handling.

I have not taken the time to implement those last two things. The first is trivial, but I believe I will more likely require a live API rather than a local program to provide that functionality. The second will come naturally, as we attempt further investigation using LLMs. (This further investigation is already underway.)

This repo contains code which tells you whether a piece of text refers to any cantos and lines, and returns those cantos and line numbers. It will soon be extended to return the lines themselves. This is an important part of 'context building'; it resolves references to The Cantos.

## Flaws

References to urcantos and pages are not handled. It’s likely we can do away with pages, but urcantos is a subtle and tricky one. At the least, our integer canto numbering doesn't handle them (though we could always offset).

When we look at the scholarship, we rarely find references to line numbers, except in the form of 'first' or 'last'. This is because there has never been a standard edition of The Cantos with line numbers. Instead, scholars have thusfar worked with page numbers, an efficient yet inaccuracte method. If we considered page numbers, we would have to annotate our digital cantos with page divisions, which is mostly or otherwise unnecessary. Cantos are either referenced as wholes or, further, as sections (Malatesta, Pisan, China, for example), or when a few lines are referenced, it is because they have been included (thus a lookup is probably not necessary). This module serves to resolve references to lines where the lines have not been included; by extension, it provides lines required to answer user queries where the user has not included those lines; the simplest example of this being, “What is the first line of Canto I?”

There is no defined behaviour for extracting line references when the canto number isn’t clear.

## Extension

The functionality this module provides could one day be extended into resolving a wider range of references, for example the content of other poems. There’s no point looking towards this now, as we’d most likely be working with a vector db (as opposed to our fundamental, `txt` source of The Cantos), but there is one instance in the training dataset of a query for Dante’s Inferno: Canto 26 in which the output (to references to Pound’s Cantos) should be empty. Whether the model achieves this or not is yet unclear.

Given that, we are probably looking at a much more complex return value, which includes author, text, and more.
