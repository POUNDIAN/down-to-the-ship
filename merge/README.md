Ideally, we would have been able to download the model from brev and run it locally (within an LMStudio Inference Server, say). The main reason behind this is cost-saving. Running models on remote servers costs money. Storing models on remote servers costs money.

Anyone who would like to make my life a little easier is invited to consider becoming a [Patreon of POUNDIAN](https://www.patreon.com/POUNDIAN).

## Harper’s Tutorial

I followed [this tutorial](https://github.com/brevdev/notebooks/blob/main/gguf-export.ipynb) by @harper-carroll to get a model offline. It only worked once. On all other attempts, the merge process got killed. This would probably be fixed if I ran an instance with more RAM, but I'm strapped and will only investigate this at a later date.

## A POUNDIAN model on my comp!?

The model that _did_ download did not perform well.

<img width="1238" alt="Screenshot_2023-12-29_at_17 07 18" src="https://github.com/POUNDIAN/down-to-the-ship/assets/1782820/2ed91011-a9b3-4e1d-9467-36a6ec464173">

[This](https://kaitchup.substack.com/p/dont-merge-your-lora-adapter-into) is the only thing I have read on the topic, and might be enough. 

> In other words, we may get a model, after merging, that performs worse than the model we had at the end of QLoRA fine-tuning.

So for now we give up on downloading and running locally, and stick with a brev deployment.
