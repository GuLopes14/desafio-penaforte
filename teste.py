import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
resposta = requests.get(url)
soup = BeautifulSoup(resposta.text, "html.parser")
print(soup.title.text)

livros = soup.find_all("article", class_="product_pod")
print(len(livros))

for livro in livros:
    titulo = livro.h3.a["title"]
    preco = livro.find("p", class_="price_color").text
    print(f"{titulo} - {preco}")

estrelas_classe = livro.find("p", class_="star-rating")["class"]
print(estrelas_classe)

estrelas = estrelas_classe[1]

mapa_estrelas = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

estrelas_numero = mapa_estrelas[estrelas]

estoque = livro.find("p", class_="instock availability").text.strip()
print(f"Estoque: {estoque}")

link = livro.h3.a["href"]

base = "https://books.toscrape.com/catalogue/"
link_completo = base + link.replace("../../../", "")

res_livro = requests.get(link_completo)
soup_livro = BeautifulSoup(res_livro.text, "html.parser")

descricao = soup_livro.find("meta", attrs={"name": "description"})["content"]

for pagina in range(1,51):
    url = f"https://books.toscrape.com/catalogue/page-{pagina}.html"