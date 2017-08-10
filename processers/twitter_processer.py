import json

from optparse import OptionParser
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from nlp.NERTagger import NERTagger
from nlp.SentimentAnalyzer import SentimentAnalyzer


def format_tweet(tweet_dict):
    tweet_formatted = {
        "id": tweet_dict.get("id"),
        "timestamp": tweet_dict.get("created_at"),
        "text": tweet_dict.get("text"),
        "user": tweet_dict.get("user", {}).get("screen_name"),
        "user_id": tweet_dict.get("user", {}).get("id"),
        "retweet": tweet_dict.get("retweeted_status", None) is not None
    }

    return tweet_formatted


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--kafka-topic", dest="kafka_topic",
                      help="Kafka topic to consume data")
    parser.add_option("-i", "--index", dest="es_index",
                      help="Elasticsearch index to send data")
    parser.add_option("-d", "--doc", dest="es_doc",
                      help="Elasticsearch doc type")
    (options, args) = parser.parse_args()

    es = Elasticsearch()
    consumer = KafkaConsumer(options.kafka_topic)
    named_entity_recognition = NERTagger('english.all.3class.distsim.crf.ser.gz', 'stanford-ner.jar')
    sentiment_analysis = SentimentAnalyzer()

    for msg in consumer:
        tweet = json.loads(msg.value.decode("utf-8"))
        tweet = format_tweet(tweet)
        tweet.update(sentiment_analysis.execute(tweet["text"]))
        tweet.update(named_entity_recognition.execute(tweet["text"]))
        res = es.index(index=options.es_index,
                       doc_type=options.es_doc,
                       id=tweet["id"],
                       body=tweet)

        print("Index status: {}. {} {}\n".format(res['created'],
                                               tweet["timestamp"],
                                               tweet["text"]))
