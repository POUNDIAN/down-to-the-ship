# And then went down to the ship

This repo contains code which tells you whether a piece of text refers to any cantos and lines, and returns those cantos and line numbers. It will soon be extended to return the lines themselves. This is an important part of 'context building'; it resolves references to The Cantos.

## Installation

Using poetry for this repo. Currently I've taken to running things from inside VSCode. If you `Cmd+P` and type `Python: Select Interpreter` you can select the poetry venv, which will fix any import errors.

This project calls a model run inside [LM Studio](https://lmstudio.ai/), available through the LMS inference server.
