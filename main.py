import requests
import json
import database
import random
from twitter_bot import Twitter_Bot

BASE_URL = "https://tv-v2.api-fetch.website/"
r = requests.get(f"{BASE_URL}movies")
assert(r.status_code == 200), f"Erro ao acessar \"{BASE_URL}\""
movie_pages = json.loads(r.content.decode(encoding="utf-8"))
MOVIE_PAGE_URL = "https://tv-v2.api-fetch.website/"

#mongodb com os filmes
bd_mongo = database.Mongo_Database()
#cria uma lista com todos os filmes disponiveis
todos_filmes = []
count_pages = len(movie_pages)
for index, page in enumerate(movie_pages):
    print(f"Consultando pagina {index + 1}/{count_pages}")
    r = None
    while ((r == None) or (r.status_code != 200)):
        r = requests.get(f"{BASE_URL}{page}")
    movies_list = json.loads(r.content.decode(encoding="utf-8"))
    todos_filmes += movies_list

#grava os filmes no mongo
#retorna os filmes novos
print(f"{len(todos_filmes)} encontrados no catalogo do Popcorn. Procurando novos titulos.")
filmes_novos = bd_mongo.grava_filmes(todos_filmes)
print(f"Foram encontrados {len(filmes_novos)} novos titulos")

if (len(filmes_novos) > 0):
    #monta um tweet com os dados do filme
    array_saudacao = [
        "Opa, encontrei novos filmes no catálogo!",
        "Tem novos filmes no Popcorn Time!"
    ]
    #saudacao randomica
    str_tweet = array_saudacao[random.randint(0, len(array_saudacao) - 1)] + "\n"
    titulos = []
    for f in filmes_novos:
        titulos.append(f["title"])
    str_tweet += f"Novos filmes: {'; '.join(titulos)}."
    #tweeta os dados dos novos filmes
    info_tweet = Twitter_Bot().tweetar(str_tweet)
    #grava o log de tweets
    if (info_tweet):
        bd_mongo.grava_tweet(info_tweet)
