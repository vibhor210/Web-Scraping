from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

df = pd.read_csv("Scraping.csv")
asin = df["Asin"]
country = df["country"]

# Storing Json data
json_data = []
for i in range(0,1000):
    if((i+1)%100 == 0):
        print(i)
    # ------------------------
    # dictionary for storing title, price, image, detail
    data = {}
    # ------------------------
    # Web-Scraping started
    url = f"https://www.amazon.{country[i]}/dp/{asin[i]}"
    headers = {
        'Referer':f"http://www.amazon.{country[i]}/dp/{asin[i]}",
        'User-Agent':'''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'''
    }
    page = requests.get(url,headers=headers)
    # ----------------------
    # Check if response is good to go
    if not page.status_code == 200:
        data["url"] = url
        data["respone"] = f"{url} is currently not available"
        json_data.append({f"{i+1}":[data]})
        continue
    soup = BeautifulSoup(page.content,"html.parser")
    # -----------------
    # Scraping title
    title = soup.find(id="productTitle")
    # -----------------
    # Scraping image
    image = soup.find(id="leftCol")
    image = image.find("img")
    # -----------------
    # Scraping price
    center = soup.find(id="centerCol")
    price = center.find("span",class_="a-size-base a-color-price")
    if price == None:
        price = center.find("span",class_="a-size-base a-color-price a-color-price")
    if price == None:
        price = center.find("span",class_="a-color-base")
    # -----------------
    # Scraping detail
    detail = []
    detailID = soup.find(id="detailBullets_feature_div")
    if detailID == None:
        detail.append("Detail Unavailable")
    else:
        ul = detailID.find("ul")
        for li in ul.findAll("li"):
            span = li.find("span")
            spantext = ""
            for s in span.findAll("span"):
                spantext = spantext+(" ".join((s.text).split()))
            spantext = spantext.replace("\u200f","")
            spantext = spantext.replace("\u200e","")
            detail.append(spantext)
    # -----------------
    # Collecting data
    data["url"] = str(url)
    data["title"] = str((title.text).strip())
    data["img"] = str(image["src"])
    if price == None:
        data["price"] = "Currently Unavailable"
    else:
        data["price"] = str(price.text)
    data["detail"] = str(detail)
    # -----------------
    # Storing data in json format
    json_data.append({f"{i+1}":[data]})


# After every 100 iteration data is bumped in json file
f = open("output.json", 'w')
f.write(json.dumps(json_data,indent=3))
f.close()
