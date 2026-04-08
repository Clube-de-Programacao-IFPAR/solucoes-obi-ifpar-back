from flask import request, Blueprint, jsonify
from ..services.questions_services import validate_answers
from ..dtos.validate_questions_dto import ValidateQuestionDTO

questions_BP = Blueprint("questions", __name__, url_prefix="/questions")

@questions_BP.route("/validate", methods=["POST"])
def validate_question():
    """
    :<json string year: The year of the question
    :<json string phase: The phase of the question
    :<json string level: The level of the question
    :<json string name: The name of the question
    :<json string filename: The name of the file with extension, must match
                            the question name and have the appropriate extension
    
    :<json string file: Contents of the file to run in the server to
                        solve the question
    
    :status 200: Returns the data of the tests applied to the file given,
                 listing time, memory usage and whether it was correct

    :status 404: Question answer folder was not found
    :status 501: File extension is not supported by the server

    .. note::
        See example ``curl`` commands at the end of the ``questions_service.py``
        file and check output there
    """
    body = request.get_json()

    submit = ValidateQuestionDTO(
        body.get("year"),
        body.get("phase"),
        body.get("level"),
        body.get("name"),
        body.get("filename"),
        body.get("file"),
    )

    response, status = validate_answers(submit)
    return jsonify(response), status
