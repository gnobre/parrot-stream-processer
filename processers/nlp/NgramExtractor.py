import re

from string import punctuation
from nltk import bigrams, trigrams
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer


class NgramExtractor:

    def __init__(self):
        self.url_re = re.compile(r"http\S+")
        self.punctuation = punctuation + '…' + "“" + "”" + "’" + "‘"
        self.translate_table = dict((ord(char), '') for char in punctuation)
        self.stopwords = stopwords.words('english') + ['via'] + ['']
        self.tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True)

    def execute(self, text):
        text = re.sub(self.url_re, "", text)
        text = text.translate(self.translate_table).strip()
        text = self.tokenizer.tokenize(text)
        text = [word for word in text if word not in self.stopwords]

        bs = list(bigrams(text))
        bs = [' '.join(b) for b in bs]

        ts = list(trigrams(text))
        ts = [' '.join(t) for t in ts]

        return {'bigrams': bs, 'trigrams': ts}
