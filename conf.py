import configparser

class Configuracoes:
    """ Singleton com as configuracoes do script """
    _instancia = None
    def __new__(cls, *args, **kwargs):
        if not(cls._instancia):
            cls._instancia = super(Configuracoes, cls).__new__(cls, *args, **kwargs)
        return cls._instancia
    
    def __init__(self,):
        self.conf = configparser.ConfigParser()
        self.conf.read("./program.conf")

    def get_config(self, sessao, chave):
        return self.conf[sessao][chave]