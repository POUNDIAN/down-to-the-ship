# Deploying this model

This model requires a GPU to run. This is because of the optimizations used, namely a 4 bit quantization, which can't be run on a CPU. Hopefully this problem will be solved later, and it will easier to run this model locally.

I use [brev.dev](https://brev.dev) to get a hold of GPUs. Spin up an A10G instance with 1 GPU and 4 CPUs. Then upload run.py and requirements.txt. If you use brev, type `brev open instance_name` in your terminal, let is open VSCode, and drag and drop the files in. 

Firstly, install the requirements.

```zsh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Then run the model with a prompt, for example:

```zsh
python run.py "What is the first line of Pound's first Canto?"
```

Expected result:

```json
{"references": [{"canto": 1, "lines": [1]}]}
```

Or:

```zsh
python run.py 'What are the first 14 lines of Pounds Canto IX?'
```

```json
{"references": [{"canto": 9, "lines": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]}]}
```

## 

Adapters stored at https://huggingface.co/poundian/down-to-the-ship

With a bit of fine-tuning, by storing our QLoRa adapters on HuggingFace (865MB), and by using GPUs made available by brev.dev, we have created a reusable model which can reliably extract references to Cantos and line numbers.
