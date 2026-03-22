import json

with open("./public/answer_urls.json", "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

def nav_years():
    return {"anos": ["2022", "2023", "2024"]}
    ...
    # {
    #     "anos": ["2022", "2023", "2024"]
    # }

def nav_phases(year: str):
    ...
    # {
    #   "ano": "2022",
    #   "fases": ["1", "2", "3"]
    # }

def nav_levels(year: str, phase: str):
    
    answer_url_levels: list = []

    if year not in json_data.keys():
        return ("Ano não encontrado", 404)
    
    elif phase not in json_data[year].keys():
        return ("Fase não encontrada", 404)

    for level in json_data[year][phase].keys():
        answer_url_levels.append(level)

    result: dict = {
        "ano": year,
        "fase": phase,
        "levels": answer_url_levels
    }

    return result

def nav_problems(year: str, phase: str, level: str):

    answer_url_problems: list = []

    if year not in json_data.keys():
        return ("Ano não encontrado", 404)
    
    elif phase not in json_data[year].keys():
        return ("Fase não encontrada", 404)
    
    elif level not in json_data[year][phase].keys():
        return ("Nível não encontrado", 404)

    for problem in json_data[year][phase][level].keys():
        answer_url_problems.append(problem)

    result: dict = {
        "ano": year,
        "fase": phase,
        "nivel": level,
        "questoes": answer_url_problems
    }

    return result
    # {
    #   "ano": "2022",
    #   "fase": "1",
    #   "nivel": "1",
    #   "questoes": ["nome", "otonome", "kaio", "AAAAAAAAAAAAAAAA"]
    # }
