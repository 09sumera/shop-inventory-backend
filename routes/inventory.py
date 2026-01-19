from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from models.product import Product

inventory_bp = Blueprint("inventory", __name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
products = db["products"]

# ---------------- ADD PRODUCT ----------------
@inventory_bp.route("/add", methods=["POST"])
def add_product():
    try:
        product = Product(request.json)
        valid, error = product.is_valid()

        if not valid:
            return jsonify({"error": error}), 400

        existing = products.find_one({"id": product.id})

        if existing:
            products.update_one(
                {"id": product.id},
                {"$inc": {"qty": product.qty}}
            )
            return jsonify({"message": "Product quantity updated"})
        else:
            products.insert_one(product.to_dict())
            return jsonify({"message": "Product added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- GET ALL PRODUCTS ----------------
@inventory_bp.route("/products", methods=["GET"])
def get_products():
    return jsonify(list(products.find({}, {"_id": 0})))


# ---------------- SELL PRODUCT ----------------
@inventory_bp.route("/sell", methods=["POST", "OPTIONS"])
def sell_product():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.json
    product = products.find_one({"id": data.get("id")})

    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product["qty"] < data.get("qty"):
        return jsonify({"error": "Insufficient stock"}), 400

    products.update_one(
        {"id": data.get("id")},
        {"$inc": {"qty": -int(data.get("qty"))}}
    )

    return jsonify({"message": "Product sold successfully"})


# ---------------- RESTOCK PRODUCT ----------------
@inventory_bp.route("/restock", methods=["POST"])
def restock_product():
    data = request.json

    products.update_one(
        {"id": data.get("id")},
        {"$inc": {"qty": int(data.get("qty"))}}
    )

    return jsonify({"message": "Product restocked"})


# ---------------- DELETE PRODUCT ----------------
@inventory_bp.route("/delete/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    products.delete_one({"id": pid})
    return jsonify({"message": "Product deleted"})


# ---------------- DASHBOARD STATS ----------------
@inventory_bp.route("/stats", methods=["GET"])
def inventory_stats():
    all_products = list(products.find({}, {"_id": 0}))

    total_products = len(all_products)
    total_quantity = sum(p["qty"] for p in all_products)
    low_stock = len([p for p in all_products if p["qty"] < 5])

    return jsonify({
        "totalProducts": total_products,
        "totalQuantity": total_quantity,
        "lowStock": low_stock,
        "products": all_products
    })
