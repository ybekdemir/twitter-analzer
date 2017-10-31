
import tweepy
import time
import config


class TwitterMiner:

    auth = None
    api = None

    def Auth(self):
        self.auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        self.auth.set_access_token(config.key, config.secret)
        self.api = tweepy.API(self.auth)


    def get_tweets_by_hashtag(self, hashtag, limit=100):
        """
        Search twitter with hashtag
        :param hashtag for search:
        :return tweetlist by given hashtag:
        """

        if hashtag == '':
            return None

        tweetList = []
        for tweet in tweepy.Cursor(self.api.search,
                                   q=hashtag,
                                   include_entities=True).items(limit):

            try:
                tweetList.append(tweet)
            except tweepy.TweepError as e:
                time.sleep(60 * 15)
                return e.reason

        return  tweetList


