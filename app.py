from flask import Flask
from flask_cors import CORS
from .routes import register_routes
from .errors import register_error_handlers

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000", "http://localhost:5173", "https://g-aleixo.github.io", "https://solucoes-obi-ifpar.onrender.com"])

app.secret_key = "Super Secret Key by Clube de Programação IFPAR"

register_routes(app)
register_error_handlers(app)

@app.get("/api/hello")
def hello():
    return {"message": "First Hello World by Flask!"}