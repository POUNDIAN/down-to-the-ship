import matplotlib.pyplot as plt

# Use this one to establish lengths (then define max-length for padding)
# def generate_and_tokenize_prompt(prompt):
#     return tokenizer(formatting_func(prompt))

# tokenized_train_dataset = train_dataset.map(generate_and_tokenize_prompt)
# tokenized_val_dataset = eval_dataset.map(generate_and_tokenize_prompt)


def plot_data_lengths(tokenized_train_dataset, tokenized_val_dataset, filename):
    lengths = [len(x['input_ids']) for x in tokenized_train_dataset]
    lengths += [len(x['input_ids']) for x in tokenized_val_dataset]
    print(len(lengths))

    # Plotting the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(lengths, bins=20, alpha=0.7, color='blue')
    plt.xlabel('Length of input_ids')
    plt.ylabel('Frequency')
    plt.title('Distribution of Lengths of input_ids')
    # plt.show()
    plt.savefig(filename)

# plot_data_lengths(tokenized_train_dataset, tokenized_val_dataset, 'data_lengths.png')
# plot_data_lengths(tokenized_train_dataset, tokenized_val_dataset, 'data_lengths_maxed.png')