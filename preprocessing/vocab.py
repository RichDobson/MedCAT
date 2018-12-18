import numpy as np
import pickle

class Vocab(object):
    def __init__(self):
        self.vocab = {}
        self.index2word = []
        self.vec_index2word = []
        self.unigram_table = []


    def add_words(self, path):
        f = open(path)

        for line in f:
            parts = line.split("\t")
            self.index2word.append(parts[0])
            self.vec_index2word.append(parts[0])

            item = {'vec': np.array([float(x)
                for x in parts[2].strip().split(" ")]), 'cnt': int(parts[1].strip())}
            self.vocab[parts[0]] = item


    def add_words_nvec(self, path, reset_cnt=True):
        f = open(path)

        for line in f:
            parts = line.split("\t")
            if parts[0] not in self.vocab:
                self.index2word.append(parts[0])

                item = {'vec': None, 'cnt': int(parts[1].strip()),
                        'ind': len(self.index2word) - 1}
                self.vocab[parts[0]] = item
            elif reset_cnt:
                # Reset the count
                self.vocab[parts[0]]['cnt'] = int(parts[1].strip())


    def make_unigram_table(self):
        prob = []
        freqs = []

        for word in self.vec_index2word:
            freqs.append(self[word])

        freqs = np.array(freqs)
        freqs = np.power(freqs, 3/4)
        sm = np.sum(freqs)

        for i, word in enumerate(self.vec_index2word):
            p = freqs[i] / sm
            self.unigram_table.extend([i] * int(p * 100000000))

        self.unigram_table = np.array(self.unigram_table)


    def get_negative_samples(self, n=6):
        inds = np.random.randint(0, len(self.unigram_table), n)

        return self.unigram_table[inds]


    def __getitem__(self, word):
        return self.vocab[word]['cnt']


    def vec(self, word):
        return self.vocab[word]['vec']


    def item(self, word):
        return self.vocab[word]


    def __contains__(self, word):
        if word in self.vocab:
            return True

        return False


    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)


    @classmethod
    def load(cls, path):
        with open(path, 'rb') as f:
            return pickle.load(f)
