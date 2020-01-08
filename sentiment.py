import torch
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pickle
import csv


# class RNN
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
        return torch.zeros(1, self.hidden_size)  # creating an instance of RNN


# rnn = RNN(EMBEDDING_DIM, HIDDEN_DIM, len(vocab), len(sentiment_class))
# loss_function = nn.NLLLoss()
# optimizer = optim.SGD(rnn.parameters(), lr=0.001)


# loading the model using pickle

filename = "../tweetmodel.pkl"

rnn = pickle.load(open('tweetmodel.pkl', 'rb'))
print(rnn)

# dataset
INPUTFILE_PATH = "Tweets.csv"

torchtweets = []
train_tweets = []
test_tweets = []
tweets = []
sentiment_class = set()
tweet_sent_class = []


def tokenizer(sentence):
    tokens = sentence.split(" ")
    tokens = [porter.stem(token.lower())
              for token in tokens if not token.lower() in stop_words]
    return tokens


porter = PorterStemmer()
stop_words = set(stopwords.words('english'))

# loading the file
i = 0
with open(INPUTFILE_PATH, 'r') as csvfile:
    tweetreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in tweetreader:        # For skipping the headerline
        if i == 0:
            i += 1
            continue
        # tweets will contain the tweet text
        tweets.append(tokenizer(row[10]))
        tweet_sent_class.append(row[1])
        sentiment_class.add(row[1])
        i += 1

sentiment_class = list(sentiment_class)

class_dict = {}

for index, class_name in enumerate(sentiment_class):
    class_dict[class_name] = index
    vocab = {}

vocab_index = 0

for tokens in tweets:
    for key, token in enumerate(tokens):
        # all_tokens.add(token)
        if token not in vocab:
            vocab[token] = vocab_index
            vocab_index += 1  # train test split


def map_word_vocab(sentence):
    idxs = [vocab[w] for w in sentence]
    return torch.tensor(idxs, dtype=torch.long)


def map_class(sentiment):
    return torch.tensor([class_dict[sentiment]], dtype=torch.long)


def prepare_sequence(sentence):
    input = map_word_vocab(sentence)
    return input


def predict(diary):
    sentence = tokenizer(diary)

    inputs = prepare_sequence(sentence)
    hidden = rnn.init_hidden()
    #         print(hidden)
    for i in range(len(inputs)):
        print(i)
        class_scores, hidden = rnn(inputs[i], hidden)
        print(class_scores)
        type(sentiment_class)
        print(sentiment_class[(class_scores.max(dim=1)[1].numpy())[0]])

    print(class_scores)
    sentiment = sentiment_class[(class_scores.max(dim=0)[1].numpy())[0]]

    if sentiment == 'negative':
        return -1
    elif sentiment == 'positive':
        return 1
    else:
        return 0
