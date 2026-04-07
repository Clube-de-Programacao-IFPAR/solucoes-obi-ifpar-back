from flask import request, Blueprint, jsonify
from ..services.search_services import search
from ..dtos.validate_search_dto import ValidateSearchDTO

search_BP = Blueprint("search", __name__, url_prefix="/search")

@search_BP.route("/", methods=["GET"])
def search_question():
    """
    :<json string year: Match with exactly the given year
    :<json string phase: Match with exactly the given phase
    :<json string level: Match with exactly the given level
    :<json string problem: Match with exactly the given problem

    :status 200: Returns a nested dictionary of the data that match the given parameters.
                 Empty data means that there was no match for a term
    
    :status 500: Server error, see the ``error`` field of response
    """
    query = ValidateSearchDTO(
        year = request.args.get("year"),
        phase = request.args.get("phase"),
        level = request.args.get("level"),
        problem = request.args.get("problem")
    )

    response, status = search(query)
    return jsonify(response), status
