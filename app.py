from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/products")
def get_products():
    try:
        res = requests.get("https://www.club72.co.uk/shop?format=json", headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
        data = res.json()

        items = []
        for item in data.get("items", []):
            if item.get("recordTypeLabel") == "store-item":
                title = item.get("title")
                url = f"https://www.club72.co.uk{item.get('fullUrl')}"
                image = item.get("assetUrl")
                variants = item.get("variants", [])
                
                # Get first variant with stock if available
                for variant in variants:
                    price = variant.get("priceMoney", {}).get("value")
                    size = variant.get("attributes", {}).get("Size")
                    stock = variant.get("qtyInStock", 0)
                    if stock > 0:
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
