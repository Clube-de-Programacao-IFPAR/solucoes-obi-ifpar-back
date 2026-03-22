import json

from ..dtos.validate_search_dto import ValidateSearchDTO

def search_by_year(data):
    return data
    
def search_by_phase(data):
    return data

def search_by_level(data):
    return data
    
def search_by_problem(data):
    return data

def search(data: ValidateSearchDTO):
    year = data["year"]
    phase = data["phase"]
    level = data["level"]
    problem = data["problem"]
    
    with open("./public/answer_urls.json", "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        
    if year is not None:
        json_data = search_by_year(json_data)
        
    if phase is not None:
        json_data = search_by_year(json_data)
        
    if level is not None:
        json_data = search_by_level(json_data)
        
    if problem is not None:
        json_data = search_by_problem(json_data)
        
    
    return {"success": 200, "data": json_data}