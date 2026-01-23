from flask import Blueprint, request, jsonify, current_app
from models.product import Product

inventory_bp = Blueprint("inventory", __name__)

# ================= HELPER =================
def products_collection():
    return current_app.config["PRODUCTS_COLLECTION"]

# ---------------- ADD PRODUCT ----------------
@inventory_bp.route("/add", methods=["POST"])
def add_product():
    try:
        product = Product(request.json)
        valid, error = product.is_valid()

        if not valid:
            return jsonify({"error": error}), 400

        products = products_collection()
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
    products = list(products_collection().find({}, {"_id": 0}))
    return jsonify(products)


# ---------------- SELL PRODUCT ----------------
@inventory_bp.route("/sell", methods=["POST", "OPTIONS"])
def sell_product():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.json
    products = products_collection()

    product = products.find_one({"id": data.get("id")})

    if not product:
        return jsonify({"error": "Product not found"}), 404

    qty = int(data.get("qty", 0))
    if product["qty"] < qty:
        return jsonify({"error": "Insufficient stock"}), 400

    products.update_one(
        {"id": data.get("id")},
        {"$inc": {"qty": -qty}}
    )

    return jsonify({"message": "Product sold successfully"})


# ---------------- RESTOCK PRODUCT ----------------
@inventory_bp.route("/restock", methods=["POST"])
def restock_product():
    data = request.json
    products = products_collection()

    products.update_one(
        {"id": data.get("id")},
        {"$inc": {"qty": int(data.get("qty"))}}
    )

    return jsonify({"message": "Product restocked"})


# ---------------- DELETE PRODUCT ----------------
@inventory_bp.route("/delete/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    products_collection().delete_one({"id": pid})
    return jsonify({"message": "Product deleted"})


# ---------------- DASHBOARD STATS ----------------
@inventory_bp.route("/stats", methods=["GET"])
def inventory_stats():
    products = list(products_collection().find({}, {"_id": 0}))

    return jsonify({
        "totalProducts": len(products),
        "totalQuantity": sum(p.get("qty", 0) for p in products),
        "lowStock": len([p for p in products if p.get("qty", 0) < 5]),
        "products": products
    })
