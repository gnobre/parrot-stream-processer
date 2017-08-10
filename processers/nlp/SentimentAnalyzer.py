from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = sid = SentimentIntensityAnalyzer()

    def execute(self, text):
        polarity_scores = self.analyzer.polarity_scores(text)

        compound = polarity_scores["compound"]

        if compound >= 0.5:
            polarity_scores["polarity"] = "positive"
        elif compound <= -0.5:
            polarity_scores["polarity"] = "negative"
        else:
            polarity_scores["polarity"] = "neutral"

        return polarity_scores
