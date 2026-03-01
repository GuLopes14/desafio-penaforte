# Desafio Web Scraping - Books to Scrape

Projeto desenvolvido como parte de um desafio técnico, com o objetivo de realizar web scraping no site [Books to Scrape](https://books.toscrape.com/) e exportar os dados coletados para um arquivo CSV.

## Funcionalidades

- Coleta dados de todos os livros disponíveis no site (todas as páginas)
- Extrai as seguintes informações de cada livro:
  - Título
  - Preço
  - Avaliação (estrelas)
  - Disponibilidade em estoque
  - Descrição
- Busca as descrições dos livros em paralelo utilizando múltiplas threads
- Salva os dados coletados em um arquivo `books.csv`

## Tecnologias utilizadas

- Python 3
- [Requests](https://pypi.org/project/requests/) — requisições HTTP
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) — parsing do HTML
- `concurrent.futures` — execução paralela com ThreadPoolExecutor
- `csv` — exportação dos dados

## Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Instale as dependências:
   ```bash
   pip install requests beautifulsoup4
   ```

3. Execute o script:
   ```bash
   python desafio.py
   ```

4. Ao finalizar, o arquivo `books.csv` será gerado na mesma pasta com todos os dados coletados.

## Estrutura do CSV gerado

| Coluna      | Descrição                        |
|-------------|----------------------------------|
| title       | Título do livro                  |
| price       | Preço                            |
| stars       | Avaliação (1 a 5)                |
| in_stock    | Disponível em estoque (True/False)|
| description | Descrição do livro               |

## Autor

Gustavo Lopes Santos da Silva
