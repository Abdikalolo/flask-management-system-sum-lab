from flask import Flask, jsonify

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
if __name__ == "__main__":
    app.run(debug=True)