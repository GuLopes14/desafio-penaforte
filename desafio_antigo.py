import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/category/books_1/index.html"

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
            #extraindo a quantidade de estrelas
            stars_class = book.find("p", class_="star-rating")["class"]
            stars_text = stars_class[1]
            stars = stars_dictionary.get(stars_text, 0)
            
            text_stock = book.find("p", class_="instock availability").text.strip()
            in_stock = "In stock" in text_stock
            
            relative_link = book.h3.a["href"]
            complete_link = BASE_URL + relative_link.replace("../../../", "")
            
            description = extract_description(complete_link)
            
            books_datas.append({
                "title": title,
                "price": price,
                "stars": stars,
                "in_stock": in_stock,
                "description": description
            })
            
        except Exception as e:
            title = book.h3.a.get("title", "Título desconhecido") if book.h3 and book.h3.a else "Título desconhecido"
            print(f"Erro ao coletar dados do livro: {title}. Erro: {e}")
            continue
    return books_datas

def save_to_csv(books_data, filename="books.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fields = ["title", "price", "stars", "in_stock", "description"]
        writer = csv.DictWriter(file, fieldnames=fields)
        
        writer.writeheader()
        writer.writerows(books_data)
    print(f"Arquivo {filename} gerado com sucesso")
    
def main():
    page = 1
    all_books = []
    
    while True:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        print(f"Coletando dados da página: {page}")
        
        soup = get_http_request(url)
        if not soup:
            break
        
        books_data = extract_books(url)
        if not books_data:
            print("Nenhum livro encontrado, encerrando a coleta.")
            break
        all_books.extend(books_data)
        page += 1        
    save_to_csv(all_books)

if __name__ == "__main__":
    main()