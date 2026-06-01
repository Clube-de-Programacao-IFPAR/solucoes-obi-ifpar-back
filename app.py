from dotenv import load_dotenv
import sys
import os
load_dotenv()
sys.path.insert(0, os.getenv("PYTHONPATH", "."))
from flask import Flask
from flask_cors import CORS
from routes import register_routes
from errors import register_error_handlers

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000", "http://localhost:5173", "https://g-aleixo.github.io", "https://solucoes-obi-ifpar.onrender.com", "https://clubeppar.github.io"])

app.secret_key = os.getenv("OBI_FLASK_SECRET")

if app.secret_key is None:
    print("Include in the .env the OBI_FLASK_SECRET")
    exit(1)

app.url_map.merge_slashes = False

register_routes(app)
register_error_handlers(app)

@app.get("/api/hello")
def hello():
    return {"message": "First Hello World by Flask!"}