# And then went down to the ship

This repo contains code which tells you whether a piece of text refers to any cantos and lines, and returns those cantos and line numbers. It will soon be extended to return the lines themselves. This is an important part of 'context building'; it resolves references to The Cantos.

## Installation

Using poetry for this repo. Currently I've taken to running things from inside VSCode. If you `Cmd+P` and type `Python: Select Interpreter` you can select the poetry venv, which will fix any import errors.

This project calls a model run inside [LM Studio](https://lmstudio.ai/), available through the LMS inference server.

To resolve lines, you need to create a `cantos/` directory that contains the cantos, each named `{roman}.txt`. Due to copyright, they can't be included here publicly. If you don’t have a `cantos` folder, the program will still extract references, but not resolve them.

## Training

Based on testing (notes in Results.md), it became clear the model required some fine-tuning. `dataset.jsonl` was created - 101 examples of text with either reference to Cantos, references to Cantos and lines, or no reference at all, taken from a range of sources including custom input (mimicking a user query), scholarship extracts (largely from the Cambridge Companion) and POUNDIAN’s [Plutarch's Eleusinian Rites](https://poundian.com/experiment/Plutarch's%20Eleusinian%20Rites) experiment (which contained line references, unlike the common scholarship which references by page).

[TheBloke’s zephyr-7B-beta-GGUF Q6](https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF) performed the best (in accuracy and efficiency) of the three models tested in Results.md, but we couldn’t train it (it doesn’t come with the files necessary for training such as `pytorch.bin` or whatever, so instead we used the [HuggingFace Zephyr](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)).

Training was performed on [brev.dev](https://brev.dev), using an NVIDIA A10G (24GiB) 1 GPUs x 4 CPUs | 16GiB. The files involved in training have been saved in the `training/` directory. The main reason for this is that there is a passive charge for storage incurred on brev.dev/AWS. We can spin up a new instance and upload the files whenever we want to use a rented instance.

Training took under an hour, and cost...

Query | Result
--- | ---
What is the first line of Pound's first Canto? | ### Answer: {"references": [{"canto": 1, "lines": [1]}]}
What is the last line of Canto II by Ezra Pound? |  ### Answer: {"references": [{"canto": 2, "lines": [-1]}]}





## Flaws

References to urcantos and pages are not handled. It’s likely we can do away with pages, but urcantos is a subtle and tricky one. At the least, our integer canto numbering doesn't handle them (though we could always offset).

When we look at the scholarship, we rarely find references to line numbers, except in the form of 'first' or 'last'. This is because there has never been a standard edition of The Cantos with line numbers. Instead, scholars have thusfar worked with page numbers, an efficient yet inaccuracte method. If we considered page numbers, we would have to annotate our digital cantos with page divisions, which is mostly or otherwise unnecessary. Cantos are either referenced as wholes or, further, as sections (Malatesta, Pisan, China, for example), or when a few lines are referenced, it is because they have been included (thus a lookup is probably not necessary). This module serves to resolve references to lines where the lines have not been included; by extension, it provides lines required to answer user queries where the user has not included those lines; the simplest example of this being, “What is the first line of Canto I?”

There is no defined behaviour for extracting line references when the canto number isn’t clear.

## Extension

The functionality this module provides could one day be extended into resolving a wider range of references, for example the content of other poems. There’s no point looking towards this now, as we’d most likely be working with a vector db (as opposed to our fundamental, `txt` source of The Cantos), but there is one instance in the training dataset of a query for Dante’s Inferno: Canto 26 in which the output (to references to Pound’s Cantos) should be empty. Whether the model achieves this or not is yet unclear.

Given that, we are probably looking at a much more complex return value, which includes author, text, and more.

## Other

One of the emotions of creating this dataset is that The Cantos aren’t actually that large. Not always.
