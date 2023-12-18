# And then went down to the ship

This repo contains code which tells you whether a piece of text refers to any cantos and lines, and returns those cantos and line numbers. It will soon be extended to return the lines themselves. This is an important part of 'context building'; it resolves references to The Cantos.

## Installation

Using poetry for this repo. Currently I've taken to running things from inside VSCode. If you `Cmd+P` and type `Python: Select Interpreter` you can select the poetry venv, which will fix any import errors.

This project calls a model run inside [LM Studio](https://lmstudio.ai/), available through the LMS inference server.

## Future

The model here trained should probably also be capable of determining references to any other poems. Especially it needs to be able to not return Pound when in fact Dante is the context. But then why not return Dante? and why not return Eliot? etc. etc. etc.

Given that, we should probably alter our training set to include author, but we can leave that for later.

## Flaws

References to urcantos and pages are not handled. It’s likely we can do away with pages, but urcantos is a subtle and tricky one. At the least, our integer canto numbering doesn't handle them. (Though we could shift them, say, to 201..208). (Are there more than 8?)

Do we really expect line numbers, or is it more likely we want to return a list of `cantos` referenced.

## Dataset

One of the emotions of creating this dataset is that The Cantos aren’t actually that large. Not always.

Observing the texts (from where references to cantos were taken as training data), most texts reference wide sections of Cantos (i.e. releases) over specific cantos. There are few page references, and very few line references.

Also haven’t tried to capture lines when Canto number is unclear. (No examples of this in the dataset, no defined way of behaving in this situation.)

