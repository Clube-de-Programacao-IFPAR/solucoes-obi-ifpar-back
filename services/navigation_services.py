import json

try:
    with open("./public/answer_urls.json", "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
except FileNotFoundError:
    json_data = {}

def nav_years() -> tuple[dict[str, str | list[str]], int]:
    try:
        answer_url_years = list(json_data.keys())
    
        return {"anos": answer_url_years}, 200
    
    except Exception as error:
        return {"error": f"Error getting years: {error}"}, 500

def nav_phases(year: str) -> tuple[dict[str, str | list[str]], int]:
    try:
        if year not in json_data:
            return {"error": "Not found year"}, 404
        
        answer_url_phases = list(json_data[year].keys())

        return {
            "ano": year,
            "phases": answer_url_phases
        }, 200

    except Exception as erro:
        return {"erro": f"Error getting phases: {erro}"}, 500

def nav_levels(year: str, phase: str) -> tuple[dict[str, str | list[str]], int]:
    try:
        if year not in json_data:
            return {"error": "Not found year"}, 404
        elif phase not in json_data[year]:
            return {"error": "Not found phase"}, 404

        answer_url_levels = list(json_data[year][phase].keys())

        return {
            "ano": year,
            "fase": phase,
            "niveis": answer_url_levels
        }, 200

    except Exception as erro:
        return {"erro": f"Error getting levels: {erro}"}, 500

def nav_problems(year: str, phase: str, level: str) -> tuple[dict[str, str | list[str]], int]:
    try:
        if year not in json_data:
            return {"error": "Not found year"}, 404
        elif phase not in json_data[year]:
            return {"error": "Not found phase"}, 404
        elif level not in json_data[year][phase]:
            return {"error": "Not found level"}, 404

        answer_url_problems = list(json_data[year][phase][level].keys())

        return {
            "ano": year,
            "fase": phase,
            "nivel": level,
            "questoes": answer_url_problems
        }, 200

    except Exception as erro:
        return {"erro": f"Error getting problems: {erro}"}, 500

def nav_problem(year: str, phase: str, level: str, problem: str) -> tuple[dict[str, str], int]:
    try:
        if year not in json_data:
            return {"error": "Not found year"}, 404
        elif phase not in json_data[year]:
            return {"error": "Not found phase"}, 404
        elif level not in json_data[year][phase]:
            return {"error": "Not found level"}, 404
        elif problem not in json_data[year][phase][level]:
            return {"error": "Not found problem"}, 404
        
        problem_flag = json_data[year][phase][level][problem][1]

        return {
            "ano": year,
            "fase": phase,
            "nivel": level,
            "questao": problem,
            "flag": problem_flag
        }, 200

    except Exception as erro:
        return {"erro": f"Error getting problem: {erro}"}, 500