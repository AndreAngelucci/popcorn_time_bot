import pymongo
from conf import Configuracoes

class Mongo_Filmes:
    """ Singleton com a conexao com o MongoDB """
    _instancia = None
    def __new__(cls, *args, **kwargs):
        if not(cls._instancia):
            cls._instancia = super(Mongo_Filmes, cls).__new__(cls, *args, **kwargs)
        return cls._instancia

    def __init__(self,):
        #pega a string de conexao no arquivo de configuracao
        string_conexao = Configuracoes().get_config("database", "string_connection")
        assert (string_conexao != ""), "String de conexao indefinida"
        try:
            self.mongo_client = pymongo.MongoClient(string_conexao)
            self.popcorn_database = self.mongo_client["popcorn_time"]
            self.collection_filmes = self.popcorn_database["filmes"]
        except:
            raise Exception("Nao foi possivel se conectar ao B.D.")
        print("Conectado a", string_conexao)
    
    def grava_filmes(self, lista_filmes):
        #verifica se o filme ja existe
        #se nao existir, grava e adiciona a lista de novos filmes
        novos = []
        try:
            for filme in lista_filmes:
                if not(self.collection_filmes.find({"_id": filme["_id"]})):
                    self.collection_filmes.insert_one(filme)
                    novos.append(filme)
        finally:            
            return novos
        
