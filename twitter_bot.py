import tweepy
from conf import Configuracoes

class Twitter_Bot:
    _instancia = None
    def __new__(cls, *args, **kwargs):
        if not(cls._instancia):
            cls._instancia = super(Twitter_Bot, cls).__new__(cls, *args, **kwargs)
        return cls._instancia

    def __init__(self):
        auth = tweepy.OAuthHandler(
            Configuracoes().get_config("twitter", "consumer_key"),
            Configuracoes().get_config("twitter", "consumer_secret")
        )
        auth.set_access_token(
            Configuracoes().get_config("twitter", "access_token"),
            Configuracoes().get_config("twitter", "access_token_secret")
        )
        self.twitter_api = tweepy.API(auth)

    def tweetar(self, str_tweet):
        self.twitter_api.update_status(str_tweet)