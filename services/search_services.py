import json

from ..dtos.validate_search_dto import ValidateSearchDTO

def search_by_year(data, year):
    year = str(year)
    if year in data:
        return {year: data[year]}
    return {}

def search_by_phase(data, phase):
    phase = str(phase)
    result = {}

    for year, year_data in data.items():
        if phase in year_data:
            result[year] = {phase: year_data[phase]}
            
    return result

def search_by_level(data, level):
    level = str(level)
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
    
def search_by_problem(data, problem):
    problem = str(problem)
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

with open("./public/answer_urls.json", "r", encoding="utf-8") as json_file:
    JSON_DATA = json.load(json_file)

def search(data: ValidateSearchDTO):
    year = data.get("year")
    phase = data.get("phase")
    level = data.get("level")
    problem = data.get("problem")
    
    json_data = JSON_DATA

    if year:
        json_data = search_by_year(json_data, year)
    if phase:
        json_data = search_by_phase(json_data, phase)
    if level:
        json_data = search_by_level(json_data, level)
    if problem:
        json_data = search_by_problem(json_data, problem)
    
    return {"success": 200, "data": json_data}