from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route("/products")
def get_products():
    url = "https://www.club72.co.uk/shop"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(r.text, "html.parser")

        script_tag = soup.find("script", id="__NEXT_DATA__")
        if not script_tag:
            return jsonify({"error": "No embedded JSON found"}), 500

        data = json.loads(script_tag.string)

        # NOTE: Structure may change – this is a sample structure
        items = []
        products = data.get("props", {}).get("pageProps", {}).get("products", [])

        for product in products:
            items.append({
                "name": product.get("title"),
                "price": product.get("variants", [{}])[0].get("price"),
                "url": f"https://www.club72.co.uk/shop/{product.get('slug')}",
                "image": product.get("assetUrl")
            })

        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
