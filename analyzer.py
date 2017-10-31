import json
from miner import  TwitterMiner
from nltk.tokenize  import  word_tokenize
import re
from collections import  Counter
import string





emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)
punctuation = list(string.punctuation)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens





class TweetAnalyzer:

    def __init__(self):
        self.counter = Counter()
        self.twitterClient = TwitterMiner()
        self.twitterClient.Auth()

    def most_common_words(self, hashtag, n):
        """
        Find most common n words which using with given hashtag

        :param hashtag: hashtag
        :param n: count of most common words related the hashtag
        :return:
        """
        tweets = self.twitterClient.get_tweets_by_hashtag(hashtag, 500)
        processedTweets = []
        for tweet in tweets:
            terms_all = [term for term in preprocess(tweet.text) if len(term)>3 and term != hashtag
                                                                    and term not in stopwords ]
            self.counter.update(terms_all)
        return self.counter.most_common(n)






analyzer = TweetAnalyzer()
print(analyzer.most_common_words("Tayyip", 8))