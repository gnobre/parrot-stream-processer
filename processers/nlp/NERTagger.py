from nltk.tag.stanford import StanfordNERTagger
from nltk.tokenize import TweetTokenizer


class NERTagger:
    def __init__(self, model_filename, path_to_jar=None, tokenizer=TweetTokenizer()):
        self.tagger = StanfordNERTagger(model_filename, path_to_jar)
        self.tokenizer = tokenizer

    def execute(self, text):
        tokens = self.tokenizer.tokenize(text)
        tags = self.tagger.tag(tokens)

        tags_dict = {"person": [],
                     "organization": [],
                     "location": []}

        for tag in tags:
            if tag[1].lower() in tags_dict.keys():
                tags_dict[tag[1].lower()].append(tag[0])

        return tags_dict
