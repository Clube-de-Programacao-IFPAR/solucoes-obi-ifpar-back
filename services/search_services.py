import json
from ..dtos.validate_search_dto import ValidateSearchDTO

try:
    with open("./public/answer_urls.json", "r", encoding="utf-8") as json_file:
        JSON_DATA = json.load(json_file)
except FileNotFoundError:
    JSON_DATA = {}

def search_by_year(data: dict, year: str) -> dict[str, dict]:
    if year in data:
        return {year: data[year]}
    return {}

def search_by_phase(data: dict, phase: str) -> dict[str, dict]:
    result = {}

    for year, year_data in data.items():
        if phase in year_data:
            result[year] = {phase: year_data[phase]}
            
    return result

def search_by_level(data: dict, level: str) -> dict[str, dict]:
    result = {}
    
    for year, year_data in data.items():
        for phase, phase_data in year_data.items():
            if level in phase_data:
                if year not in result:
                    result[year] = {}
                if phase not in result[year]:
                    result[year][phase] = {}

                result[year][phase][level] = phase_data[level]
    
    return result
    
def search_by_problem(data: dict, problem: str) -> dict[str, dict]:
    result = {}
    
    for year, year_data in data.items():
        for phase, phase_data in year_data.items():
            for level, level_data in phase_data.items():
                if problem in level_data:
                    if year not in result:
                        result[year] = {}
                    if phase not in result[year]:
                        result[year][phase] = {}
                    if level not in result[year][phase]:
                        result[year][phase][level] = {}
                    
                    result[year][phase][level][problem] = level_data[problem]
    
    return result

def search(data: ValidateSearchDTO) -> tuple[dict[str, dict | str], int]:
    try:
        year = data.year
        phase = data.phase
        level = data.level
        problem = data.problem
        
        json_data = JSON_DATA

        if year:
            json_data = search_by_year(json_data, year)
        if phase:
            json_data = search_by_phase(json_data, phase)
        if level:
            json_data = search_by_level(json_data, level)
        if problem:
            json_data = search_by_problem(json_data, problem)
        
        return {"data": json_data}, 200
    
    except Exception as error:
        return {"error": f"Error getting this search: {error}"}, 500