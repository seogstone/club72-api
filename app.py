from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/products")
def scrape():
    url = "https://www.club72.co.uk/shop"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    products = []

    for item in soup.select('.product-grid-item'):
        name = item.select_one('.woocommerce-loop-product__title')
        price = item.select_one('.woocommerce-Price-amount')
        link = item.select_one('a')
        image = item.select_one('img')

        if name and price and link:
            products.append({
                "name": name.text.strip(),
                "price": price.text.strip(),
                "url": link['href'],
                "image": image['src'] if image else None
            })

    return jsonify(products)
