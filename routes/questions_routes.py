from flask import request, Blueprint, jsonify
from ..services.questions_services import validate_answers
from ..dtos.validate_questions_dto import ValidateQuestionDTO

questions_BP = Blueprint("questions", __name__, url_prefix="/questions")

@questions_BP.route("/validate", methods=["POST"])
def validate_question():
    body = request.get_json()

    submit = ValidateQuestionDTO(
        year = body.get("year"),
        phase = body.get("phase"),
        level = body.get("level"),
        name = body.get("name"),
        filename = body.get("filename"),
        file = body.get("file"),
    )

    error = submit.validate()
    if error:
        return error

    response, status = validate_answers(submit)
    return jsonify(response), status
