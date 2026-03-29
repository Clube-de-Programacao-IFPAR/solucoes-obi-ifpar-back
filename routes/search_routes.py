from flask import request, Blueprint, jsonify
from ..services.search_services import search
from ..dtos.validate_search_dto import ValidateSearchDTO

search_BP = Blueprint("search", __name__, url_prefix="/search")

@search_BP.route("/", methods=["GET"])
def search_question():
    query = ValidateSearchDTO(
        year = request.args.get("year"),
        phase = request.args.get("phase"),
        level = request.args.get("level"),
        problem = request.args.get("problem")
    )

    error = query.validate()
    if error:
        return error

    response, status = search(query)
    return jsonify(response), status
