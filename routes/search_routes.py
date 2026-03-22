from flask import request, Blueprint
from ..services.search_services import search

search_BP = Blueprint("search", __name__, url_prefix="/search")

@search_BP.route("/", methods=["GET"])
def search_question():
    query = {}
    
    year = request.args.get("year", default="", type=str)
    query["year"] = year
    
    phase = request.args.get("phase", default="", type=str)
    query["phase"] = phase
    
    level = request.args.get("level", default="", type=str)
    query["level"] = level
    
    problem = request.args.get("problem", default="", type=str)
    query["problem"] = problem
    
    data = search(query)
    
    return data