import pymongo
from conf import Configuracoes

class Mongo_Database:
    """ Singleton com a conexao com o MongoDB """
    _instancia = None
    def __new__(cls, *args, **kwargs):
        if not(cls._instancia):
            cls._instancia = super(Mongo_Database, cls).__new__(cls, *args, **kwargs)
        return cls._instancia

    def __init__(self,):
        #pega a string de conexao no arquivo de configuracao
        string_conexao = Configuracoes().get_config("database", "string_connection")
        assert (string_conexao != ""), "String de conexao indefinida"
        try:
            self.mongo_client = pymongo.MongoClient(string_conexao)            
            self.collection_filmes = self.mongo_client["popcorn_time"]["filmes"]
            self.collection_tweets = self.mongo_client["twitter_log"]["tweets"]
        except:
            raise Exception("Nao foi possivel se conectar ao B.D.")
        print("Conectado a", string_conexao)
    
    def grava_filmes(self, lista_filmes):
        #verifica se o filme ja existe
        #se nao existir, grava e adiciona a lista de novos filmes
        novos = []
        try:
            for filme in lista_filmes:
                if (self.collection_filmes.count_documents({"_id": filme["_id"]}) == 0):
                    self.collection_filmes.insert_one(filme)
                    novos.append(filme)
        finally:            
            return novos

    def grava_tweet(self, tweet_info):
        #grava o retorno dos tweets
        self.collection_tweets.insert_one(tweet_info)        
