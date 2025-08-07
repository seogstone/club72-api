from flask import Flask, jsonify
import requests
import re
from html import unescape

app = Flask(__name__)

@app.route("/products")
def get_products():
    try:
        res = requests.get("https://www.club72.co.uk/shop?format=json", headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
        data = res.json()

        items = []

        for item in data.get("items", []):
            if item.get("recordTypeLabel") != "store-item":
                continue

            title = item.get("title")
            url = f"https://www.club72.co.uk{item.get('fullUrl')}"
            image = item.get("assetUrl")
            excerpt_html = item.get("excerpt", "")
            excerpt_text = unescape(excerpt_html.replace("<br>", "\n"))
            size_from_excerpt = None

            # Extract size from excerpt using regex
            match = re.search(r"Size\s*[-:]?\s*([^\n<]+)", excerpt_text)
            if match:
                size_from_excerpt = match.group(1).strip()

            variants = item.get("variants", [])
            for variant in variants:
                stock = variant.get("qtyInStock", 0)
                if stock <= 0:
                    continue

                # Use size from structured data if available
                size = variant.get("attributes", {}).get("Size") or size_from_excerpt
                price = variant.get("priceMoney", {}).get("value")

                items.append({
                    "name": title,
                    "price": price,
                    "size": size,
                    "in_stock": stock,
                    "url": url,
                    "image": image
                })

        return jsonify(items)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
