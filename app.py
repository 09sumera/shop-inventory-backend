from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

from routes.inventory import inventory_bp

app = Flask(__name__)
CORS(app)

# ---------------- MONGODB CONNECTION ----------------
MONGO_URI = os.environ.get("MONGO_URI")

# Local fallback (safe for dev)
if not MONGO_URI:
    MONGO_URI = "mongodb+srv://Sumera:Sumera0904@cluster0.n6amxue.mongodb.net/inventory_db"

client = MongoClient(MONGO_URI)
db = client["inventory_db"]
products = db["products"]

# Share collection with blueprint
app.config["PRODUCTS_COLLECTION"] = products

# Register blueprint
app.register_blueprint(inventory_bp)

# Health check only
@app.route("/")
def home():
    return jsonify({"status": "Backend running"})

if __name__ == "__main__":
    app.run(debug=True)
