# down to the ship

Experiment write-up: [POUNDIAN / down-to-the-ship](https://poundian.com/experiments/down-to-the-ship)

View `deploy` for instructions on running the model.

This repo contains code which tells you whether a piece of text refers to any cantos and lines, and returns those cantos and line numbers. It will soon be extended to return the lines themselves. This is an important part of 'context building'; it resolves references to The Cantos.

## Installation

Using poetry for this repo. Currently I've taken to running things from inside VSCode. If you `Cmd+P` and type `Python: Select Interpreter` you can select the poetry venv, which will fix any import errors.

This project calls a model run inside [LM Studio](https://lmstudio.ai/), available through the LMS inference server.

To resolve lines, you need to create a `cantos/` directory that contains the cantos, each named `{roman}.txt`. Due to copyright, they can't be included here publicly. If you don’t have a `cantos` folder, the program will still extract references, but not resolve them.


## Flaws

References to urcantos and pages are not handled. It’s likely we can do away with pages, but urcantos is a subtle and tricky one. At the least, our integer canto numbering doesn't handle them (though we could always offset).

When we look at the scholarship, we rarely find references to line numbers, except in the form of 'first' or 'last'. This is because there has never been a standard edition of The Cantos with line numbers. Instead, scholars have thusfar worked with page numbers, an efficient yet inaccuracte method. If we considered page numbers, we would have to annotate our digital cantos with page divisions, which is mostly or otherwise unnecessary. Cantos are either referenced as wholes or, further, as sections (Malatesta, Pisan, China, for example), or when a few lines are referenced, it is because they have been included (thus a lookup is probably not necessary). This module serves to resolve references to lines where the lines have not been included; by extension, it provides lines required to answer user queries where the user has not included those lines; the simplest example of this being, “What is the first line of Canto I?”

There is no defined behaviour for extracting line references when the canto number isn’t clear.

## Extension

The functionality this module provides could one day be extended into resolving a wider range of references, for example the content of other poems. There’s no point looking towards this now, as we’d most likely be working with a vector db (as opposed to our fundamental, `txt` source of The Cantos), but there is one instance in the training dataset of a query for Dante’s Inferno: Canto 26 in which the output (to references to Pound’s Cantos) should be empty. Whether the model achieves this or not is yet unclear.

Given that, we are probably looking at a much more complex return value, which includes author, text, and more.

## Other

One of the emotions of creating this dataset is that The Cantos aren’t actually that large. Not always.
