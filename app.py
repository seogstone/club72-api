from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/products")
def get_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.club72.co.uk/shop", timeout=60000)

        page.wait_for_selector("li.product", timeout=10000)
        product_elements = page.query_selector_all("li.product")

        products = []

        for item in product_elements:
            name = item.query_selector("h2.woocommerce-loop-product__title")
            price = item.query_selector("span.woocommerce-Price-amount")
            link = item.query_selector("a")
            image = item.query_selector("img")

            if name and price and link:
                products.append({
                    "name": name.inner_text().strip(),
                    "price": price.inner_text().strip(),
                    "url": link.get_attribute("href"),
                    "image": image.get_attribute("src") if image else None
                })

        browser.close()
        return jsonify(products)
