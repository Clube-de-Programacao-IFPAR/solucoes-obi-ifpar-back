from flask import request, Blueprint, jsonify
from ..services.search_services import search

search_BP = Blueprint("search", __name__, url_prefix="/search")

@search_BP.route("/", methods=["GET"])
def search_question():
    query = {
        "year": request.args.get("year", default="", type=str),
        "phase": request.args.get("phase", default="", type=str),
        "level": request.args.get("level", default="", type=str),
        "problem": request.args.get("problem", default="", type=str),
    }
    
    data = search(query)
    
    return jsonify(data)