from flask import request, Blueprint 
from ..services import questions_services

questions_BP = Blueprint("questions", __name__, url_prefix="/questions")

@questions_BP.route("/validate", methods=["POST"])
def validate_question():
    data, status = questions_services.validate_answers(request.get_json())
    return data, status