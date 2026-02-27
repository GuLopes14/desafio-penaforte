import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://books.toscrape.com/catalogue/"
MAX_WORKERS = 30

stars_dictionary = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def get_http_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar a URL: {url}")
        return None
    return BeautifulSoup(response.text, "html.parser")

def extract_description(url):
    soup = get_http_request(url)
    if not soup:
        return "Descrição não encontrada"

    description_tag = soup.find("meta", attrs={"name": "description"})
    if description_tag:
        return description_tag["content"].strip()
    return "Sem descrição"


def extract_books(url):
    soup = get_http_request(url)
    if not soup:
        return []
    books = soup.find_all("article", class_="product_pod")
    books_datas = []

    for book in books:
        try:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            # extraindo a quantidade de estrelas
            stars_class = book.find("p", class_="star-rating")["class"]
            stars = stars_dictionary.get(stars_class[1], 0)

            text_stock = book.find("p", class_="instock availability").text.strip()
            in_stock = "In stock" in text_stock

            relative_link = book.h3.a["href"]
            complete_link = BASE_URL + relative_link.replace("../../../", "")

            books_datas.append({
                "title": title,
                "price": price,
                "stars": stars,
                "in_stock": in_stock,
                "link": complete_link
            })

        except Exception as e:
            title = book.h3.a.get("title", "Título desconhecido") if book.h3 and book.h3.a else "Título desconhecido"
            print(f"Erro ao coletar dados do livro: {title}. Erro: {e}")
    return books_datas


def fetch_description_for_book(book):
    
    # Busca a descrição de um livro e retorna o dicionário completo.
    book["description"] = extract_description(book.pop("link"))
    return book

def save_to_csv(books_data, filename="books.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fields = ["title", "price", "stars", "in_stock", "description"]
        writer = csv.DictWriter(file, fieldnames=fields)
        
        writer.writeheader()
        writer.writerows(books_data)
    print(f"Arquivo {filename} gerado com sucesso")
    
def main():
    page = 1
    all_books_raw = []

    # Coleta dados básicos de todas as páginas sequencialmente
    while True:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        print(f"Coletando página {page}...")

        books_raw = extract_books(url)
        if not books_raw:
            print("Coleta de páginas concluída.")
            break

        all_books_raw.extend(books_raw)
        page += 1

    # Busca todas as descrições em paralelo
    print(f"\nBuscando descrições de {len(all_books_raw)} livros em paralelo ({MAX_WORKERS} threads)...")
    all_books = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_description_for_book, book): book for book in all_books_raw}

        for i, future in enumerate(as_completed(futures), 1):
            try:
                all_books.append(future.result())
                print(f"Descrições obtidas: {i}/{len(all_books_raw)}", end="\r")
            except Exception as e:
                print(f"Erro ao buscar descrição: {e}")

    print()
    save_to_csv(all_books)

if __name__ == "__main__":
    main()