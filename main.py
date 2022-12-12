import requests, json
from bs4 import BeautifulSoup
import pandas as pd

url: str = "https://quotes.toscrape.com"

headers:dict = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

def get_quotes(url: str):
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        soup:BeautifulSoup = BeautifulSoup(res.text, "html.parser")
        
        # proses scraping
        content = soup.find_all("div", {"class": "quote"})
        quotes_list = []
        for con in content:
            quotes = con.find("span", {"class": "text"}).text.strip()
            author = con.find("small", {"class": "author"}).text.strip()
            author_detail = con.find("a")["href"]

            data: dict = {
                "quotes": quotes,
                "quoted by": author,
                "author detail": url + author_detail
            }
            quotes_list.append(data)
        
        # proses mengolahan data
        with open("result.json", "w+") as f:
            json.dump(quotes_list, f)

        print("data berhasil diolah")

        return quotes_list

def get_detail(detail_url: str):
    res = requests.get(detail_url, headers=headers)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")

        # proses scraping
        author_name = soup.find("h3", {"class": "author-title"}).text
        born_date = soup.find("span", {"class": "author-born-date"}).text
        born_location = soup.find("span", {"class": "author-born-location"}).text
        description = soup.find("div",{"class": "author-description"}).text

        # proses mapping
        data: dict = {
            "author": author_name,
            "date of birth": born_date,
            "born location": born_location,
            "description": description
        }

        return data

def generate_format(filename: str, results: list):
    df = pd.DataFrame(results)

    if ".csv" or ".xlsx" in filename:
        df.to_csv(filename + ".csv", index=False)
        df.to_excel(filename + ".xlsx", index=False)
    
    print("data generated")

def crawling():
    result: list[dict[str, str]] = []

    quotes: list = get_quotes(url=url)
    for quote in quotes:
        detail = get_detail(detail_url=quote['author detail'])

        final_result: dict = {**quote, **detail}
        
        result.append(final_result)

    generate_format(filename= "report", results=result)

if __name__ == "__main__":
    crawling()