import requests
import json
import database
import random

BASE_URL = "https://tv-v2.api-fetch.website/"
r = requests.get(f"{BASE_URL}movies")
assert(r.status_code == 200), f"Erro ao acessar \"{BASE_URL}\""
movie_pages = json.loads(r.content.decode(encoding="utf-8"))
MOVIE_PAGE_URL = "https://tv-v2.api-fetch.website/"

#mongodb com os filmes
database_filmes = database.Mongo_Filmes()
#cria uma lista com todos os filmes disponiveis
todos_filmes = []
count_pages = len(movie_pages)
for index, page in enumerate(movie_pages):
    print(f"Consultando pagina {index}/{count_pages}")
    r = None
    while ((r == None) or (r.status_code != 200)):
        r = requests.get(f"{BASE_URL}{page}")
    movies_list = json.loads(r.content.decode(encoding="utf-8"))
    todos_filmes += movies_list

#grava os filmes no mongo
#retorna os filmes novos
filmes_novos = database_filmes.grava_filmes(todos_filmes)
print(f"Foram encontrados {len(filmes_novos)} novos filmes")

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
print(str_tweet)