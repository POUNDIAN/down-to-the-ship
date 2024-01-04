# Training

## First Attempt

Based on testing (notes in Results.md), it became clear the model required some fine-tuning. `dataset.jsonl` was created - 101 examples of text with either reference to Cantos, references to Cantos and lines, or no reference at all, taken from a range of sources including custom input (mimicking a user query), scholarship extracts (largely from the Cambridge Companion) and POUNDIAN’s [Plutarch's Eleusinian Rites](https://poundian.com/experiment/Plutarch's%20Eleusinian%20Rites) experiment (which contained line references, unlike the common scholarship which references by page).

[TheBloke’s zephyr-7B-beta-GGUF Q6](https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF) performed the best (in accuracy and efficiency) of the three models tested in Results.md, but we couldn’t train it (it doesn’t come with the files necessary for training such as `pytorch.bin` or whatever, so instead we used the [HuggingFace Zephyr](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)).

Training was performed on [brev.dev](https://brev.dev), using an NVIDIA A10G (24GiB) 1 GPUs x 4 CPUs | 16GiB. The files involved in training have been saved in the `training/` directory. The main reason for this is that there is a passive charge for storage incurred on brev.dev/AWS. We can spin up a new instance and upload the files whenever we want to use a rented instance.

Training took under an hour, and cost...

Query | Result
--- | ---
What is the first line of Pound's first Canto? | ### Answer: {"references": [{"canto": 1, "lines": [1]}]}
What is the last line of Canto II by Ezra Pound? |  ### Answer: {"references": [{"canto": 2, "lines": [-1]}]}

Actually those results aren't true to it. Firstly, there was this question chaining which was solved by the next iteration.

### PAD token

Thanks to "'Ken' a.k.a. 'Frosty'" on the brev.dev Discord.

https://www.georgesung.com/ai/qlora-ift/
https://github.com/georgesung/llm_qlora/blob/7cd7ad343cf704307ef3661a14823d219f497ed7/QloraTrainer.py#L29
https://github.com/huggingface/transformers/issues/22794
https://gist.github.com/younesbelkada/9f7f75c94bdc1981c8ca5cc937d4a4da

Basically `tokenizer.pad_token = tokenizer.eos_token` becomes `tokenizer.pad_token = "[PAD]"`.

After this change, a run of the model doesn't result in auto-generated prompts following the first result (a series of unwanted prompts and responses after the first response).

### Checkpoint Choice

I am choosing the checkpoint with least loss and least runtime.

### Thus far

```
eval_prompt = "In the fourth line of Ezra Pound’s first Canto"
```

The above prompt gives the following output:

```
In the fourth line of Ezra Pound’s first Canto, he writes: “I cannot make it cohere” (1994: 3). This is a highly significant statement for two reasons. Firstly, it refers to Pound’s own poetic project, The Cantos, and suggests that he is aware of its difficulties, both in terms of coherence and composition. Secondly, it can be read as a comment on the state of Europe after the First World War; Pound is admitting that he cannot reconc
```

I mean this is the fundamental behaviour of an LLM; it is a auto-completion device. So. Should we be escaping LLMs and going back to bert-like models? Or can we build a better context to avoid this? e.g. we were wrapping prompts in `"` to emphasise them being quotes over prompts.

- view tests.txt for success

# brev issues

So twice I have lost my files on the brev instance, incurring extra time and financial cost, because I have to retrain. I suspect the problem is that I am clicking the all-too-clickable 'Build' on the instance page, instead of 'Start', thus rebuilding my instance and removing all progress stored on it.

The checkpoints are really large files, and downloading them all is impractical. There is also the issue that we can't run `run.py` locally because it involves quantization, and I don't have a GPU. SO what we want to do is resolve all those problems: make the model locally runable, without downloading checkpoints, and avoid storing files on brev (which also costs a lot of money).

I asked ChatGPT and got [this answer](https://chat.openai.com/share/a6968336-1bf4-4fc8-9d76-bfa878f9d734). Which I'm now following.

The checkpoint contains 865MB of `adapter_model.safetensors` and 170MB of `optimizer.pt`. In run.py we do

```python
tokenizer = AutoTokenizer.from_pretrained(base_model_id, add_bos_token=True, trust_remote_code=True)

ft_model = PeftModel.from_pretrained(base_model, "zephyr-cantos/checkpoint-425")
```

and by running `ft_model.save_pretrained('dtts-trained')`, we produce an `adapter_model.safetensors` of 600MB, which shows our memory savings by using Peft?

Anyway, hopefully that `ft_model.save` will provide us with something we can run locally. At the very least, it provides us with something we can upload to HuggingFace, i.e. store elsewhere and pick up later for quantization or whatever.

## Merging?

> In other words, we may get a model, after merging, that performs worse than the model we had at the end of QLoRA fine-tuning.

From here: https://kaitchup.substack.com/p/dont-merge-your-lora-adapter-into

It's true. View the screenshot or play with the local model. Even with a system prompt, it couldn't provide simple JSON as requested like the unmerged model could do while still on the instance.

So merging isn't the way forward. It looks like we are just supposed to move our adapters around, leaving the base model alone.

_Wait_, I think we can't do this, because we don't have a local GPU. When we want to use quantization features such as `load_in_4bit`, we must be on brev; these features are GPU only.

Conclusion? We leave for brev, for now, until the taxman allows us to quantize locally.
