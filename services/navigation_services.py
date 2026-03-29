import json

try:
    with open("./public/answer_urls.json", "r", encoding="utf-8") as json_file:
        JSON_DATA = json.load(json_file)
except FileNotFoundError:
    JSON_DATA = {}

def validate(year=None, phase=None, level=None, problem=None):
    if year:
        if not year.isdigit():
            return {"error": "Invalid year format"}, 400
        if year not in JSON_DATA:
            return {"error": "Year not found"}, 404

    if phase:
        if phase not in ("c", "1", "2", "3"):
            return {"error": "Invalid phase format"}, 400
        if phase not in JSON_DATA[year]:
            return {"error": "Phase not found"}, 404

    if level:
        if level not in ("j", "1", "2", "s", "u"):
            return {"error": "Invalid level format"}, 400
        if level not in JSON_DATA[year][phase]:
            return {"error": "Level not found"}, 404

    if problem:
        if problem not in JSON_DATA[year][phase][level]:
            return {"error": "Problem not found"}, 404

    return None

def nav_years() -> tuple[dict[str, str | list[str]], int]:
    try:
        answer_url_years = list(JSON_DATA.keys())
    
        return {"anos": answer_url_years}, 200
    
    except Exception as error:
        return {"error": f"Error getting years: {error}"}, 500

def nav_phases(year: str) -> tuple[dict[str, str | list[str]], int]:
    try:
        error = validate(year)
        if error:
            return error
        
        answer_url_phases = list(JSON_DATA[year].keys())

        return {
            "ano": year,
            "fases": answer_url_phases
        }, 200

    except Exception as erro:
        return {"error": f"Error getting phases: {erro}"}, 500

def nav_levels(year: str, phase: str) -> tuple[dict[str, str | list[str]], int]:
    try:
        error = validate(year, phase)
        if error:
            return error

        answer_url_levels = list(JSON_DATA[year][phase].keys())

        return {
            "ano": year,
            "fase": phase,
            "niveis": answer_url_levels
        }, 200

    except Exception as erro:
        return {"error": f"Error getting levels: {erro}"}, 500

def nav_problems(year: str, phase: str, level: str) -> tuple[dict[str, str | list[str]], int]:
    try:
        error = validate(year, phase, level)
        if error:
            return error

        answer_url_problems = list(JSON_DATA[year][phase][level].keys())

        return {
            "ano": year,
            "fase": phase,
            "nivel": level,
            "questoes": answer_url_problems
        }, 200

    except Exception as erro:
        return {"error": f"Error getting problems: {erro}"}, 500

def nav_problem(year: str, phase: str, level: str, problem: str) -> tuple[dict[str, str], int]:
    try:
        error = validate(year, phase, level, problem)
        if error:
            return error
        
        problem_url, problem_flag = JSON_DATA[year][phase][level][problem]

        return {
            "ano": year,
            "fase": phase,
            "nivel": level,
            "questao": problem,
            "url": problem_url,
            "flag": problem_flag
        }, 200

    except Exception as erro:
        return {"error": f"Error getting problem: {erro}"}, 500
