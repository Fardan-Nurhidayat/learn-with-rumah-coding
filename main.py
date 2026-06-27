import requests
from bs4 import BeautifulSoup
import time # Untuk melimit rate
import pandas as pd


def scrap_city(city , url , page=1):
    print("mulai melakukan scraping")
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0: Win64; x64)"
    }
    response = requests.get(url + f"?page=" , headers=headers)
    soup = BeautifulSoup(response.text , "html.parser")

    container = soup.find("div" , {"class" : "order-3"})

    # Ambil semua elemen rumah
    featured = container.find_all("div" , {"class" : "propertyCardRoot"})
    # The columns for content is "propertyCardSrpContent"
    data = []
    for idx , house in enumerate(featured):
        # Take a container from every house
        content = house.find("div" , {"class" : "propertyCardSrpContent"})

        if content is None:
            continue
        price = content.find("div" , {"data-name" : "price-info"}).text.strip()
        name = content.find("a" , {"class" : "propertyCardTitleCover"}).text.strip()
        address = content.find("p" , {"class" : "propertyCardLocationRoot px-4"}).text.strip()

        attribute = content.find("div" , {"class" : "propertyCardAttributesRoot"})

        # Ambil child ke 1 pada attribute
        bedroom = attribute.find_all("span")[0].text.strip()
        bathroom = attribute.find_all("span")[1].text.strip()
        # Cek apakah ada garasi atau tidak
        garage = attribute.find_all("span")[2].text.strip() if len(attribute.find_all("span")) == 7 else 0
        surface_area = attribute.find_all("span")[3].text.strip()
        building_area = attribute.find_all("span")[5].text.strip()
        data.append(
            {
                "city" : city ,
                "name" : name ,
                "price" : price ,
                "address" : address ,
                "bedroom" : bedroom ,
                "bathroom" : bathroom ,
                "garage" : garage ,
                "surface_area" : surface_area ,
                "building_area" : building_area
            }
        )
    time.sleep(3)
    print(f"Selesai melakukan scraping halaman ke-{page}")
    return data;

cities = {
    "Jakarta Timur" : "https://www.rumah123.com/jual/jakarta-timur/rumah/",
}

def start_scraping(cities , max_page_per_city=10):
    data = []
    for city , url in cities.items():
        for page in range(1 , max_page_per_city + 1):
            page_data = scrap_city(city , url , page)
            data.extend(page_data)
    return data

data = start_scraping(cities)

# Save to csv
df = pd.DataFrame(data)
df.to_csv("data.csv" , index=False)