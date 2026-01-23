from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

from routes.inventory import inventory_bp

# ---------------- CREATE APP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- MONGODB CONNECTION ----------------
# Works both locally and on Render
MONGO_URI = os.environ.get("MONGO_URI")

# 🔹 Local fallback (safe for development)
if not MONGO_URI:
    MONGO_URI = "mongodb+srv://Sumera:Sumera0904@cluster0.n6amxue.mongodb.net/inventory_db"

client = MongoClient(MONGO_URI)
db = client["inventory_db"]
products = db["products"]

# 🔑 Share Mongo collection with blueprints
app.config["PRODUCTS_COLLECTION"] = products

# ---------------- REGISTER BLUEPRINT ----------------
app.register_blueprint(inventory_bp)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return jsonify({"status": "Backend running"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
