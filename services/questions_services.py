from ..dtos import validate_questions_dto

def validate_answers(data: validate_questions_dto ): 
    question_year = data.get("year")
    question_level = data.get("level")
    question_name = data.get("name")
    
    ## Lógica de validação 

    return {"sucess": 200, "message": "It worked!", "data": data}