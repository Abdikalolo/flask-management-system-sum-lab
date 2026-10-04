from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "barcode": "3017620422003",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "quantity": 20,
        "price": 450
    },
    {
        "id": 2,
        "barcode": "5449000000996",
        "product_name": "Coca-Cola Original",
        "brands": "Coca-Cola",
        "ingredients_text": "Carbonated water, sugar, flavourings",
        "quantity": 50,
        "price": 150
    },
    {
        "id": 3,
        "barcode": "5000159484695",
        "product_name": "Cadbury Dairy Milk",
        "brands": "Cadbury",
        "ingredients_text": "Milk, sugar, cocoa butter, cocoa mass",
        "quantity": 30,
        "price": 200
    }
] 
def fetch_openfoodfacts(query, search_type="barcode"):
    headers = {
        "User-Agent": "InventoryManagementApp/1.0 (student project)"
    }

    if search_type == "barcode":
        url = f"https://world.openfoodfacts.org/api/v2/product/{query}.json"

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("status") != 1:
            return None

        product = data.get("product", {})

        return {
            "barcode": product.get("code", query),
            "product_name": product.get("product_name", ""),
            "brands": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", "")
        }

    if search_type == "name":
        url = "https://world.openfoodfacts.org/api/v2/search"

        params = {
            "search_terms": query,
            "fields": "code,product_name,brands,ingredients_text",
            "page_size": 10
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        products = data.get("products", [])

        return [
            {
                "barcode": product.get("code", ""),
                "product_name": product.get("product_name", ""),
                "brands": product.get("brands", ""),
                "ingredients_text": product.get("ingredients_text", "")
            }
            for product in products
            if product.get("product_name")
        ]

    return None

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    required_fields = [
        "product_name",
        "brands",
        "ingredients_text",
        "quantity",
        "price"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    new_id = max((item["id"] for item in inventory), default=0) + 1

    new_item = {
        "id": new_id,
        "barcode": data.get("barcode", ""),
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data["ingredients_text"],
        "quantity": data["quantity"],
        "price": data["price"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Provide at least one field to update"}), 400

    allowed_fields = [
        "barcode",
        "product_name",
        "brands",
        "ingredients_text",
        "quantity",
        "price"
    ]

    for field in data:
        if field not in allowed_fields:
            return jsonify({"error": f"Invalid field: {field}"}), 400

    item.update(data)

    return jsonify(item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)

    return jsonify({"message": "Item deleted successfully"}), 200

@app.route("/external-products/barcode/<string:barcode>", methods=["GET"])
def search_by_barcode(barcode):
    product = fetch_openfoodfacts(barcode, search_type="barcode")

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200

@app.route("/external-products/search", methods=["GET"])
def search_by_name():
    name = request.args.get("name", "").strip()

    if not name:
        return jsonify({"error": "Please provide a product name"}), 400

    products = fetch_openfoodfacts(name, "name")

    if products is None:
        return jsonify({"error": "Search failed"}), 500

    return jsonify({
        "products": products,
        "total": len(products)
    }), 200

@app.route("/inventory/import", methods=["POST"])
def import_product():
    data = request.get_json()

    if not data or "barcode" not in data:
        return jsonify({"error": "Barcode is required"}), 400

    product = fetch_openfoodfacts(data["barcode"], "barcode")

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    new_id = max((item["id"] for item in inventory), default=0) + 1

    product["id"] = new_id
    product["quantity"] = data.get("quantity", 1)
    product["price"] = data.get("price", 0)

    inventory.append(product)

    return jsonify(product), 201

if __name__ == "__main__":
    app.run(debug=True)