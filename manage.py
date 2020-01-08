#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import torch
from nltk.corpus import words
from nltk.stem import PorterStemmer
import torch.nn as nn


class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, vocab_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.word_embeddings = nn.Embedding(vocab_size, input_size)
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, word, hidden):
        embeds = self.word_embeddings(word)
        combined = torch.cat((embeds.view(1, -1), hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.hidden_size)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turningpages.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
