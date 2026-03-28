import json

with open("./public/answer_urls.json", "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

def nav_years():
    try:
        answer_url_years = []
        for year in json_data.keys():
            answer_url_years.append(year)

        return {"anos": answer_url_years}, 200
    
    except Exception as erro:
        return {"erro": f"Erro na busca de anos: {erro}"}, 500

def nav_phases(year: str): 
    try:
        answer_url_phases: list = []

        if year not in json_data.keys():
            return ("Ano não encontrado", 404)
        
        for phase in json_data[year].keys():
            answer_url_phases.append(phase)

        return {
            "ano": year,
            "phases": answer_url_phases
        }, 200

    except Exception as erro:
        return {"erro": f"Erro na busca de fases por ano: {erro}"}, 500


def nav_levels(year: str, phase: str):
    try:
        answer_url_levels: list = []

        if year not in json_data.keys():
            return ("Ano não encontrado", 404)
        
        elif phase not in json_data[year].keys():
            return ("Fase não encontrada", 404)

        for level in json_data[year][phase].keys():
            answer_url_levels.append(level)

        return {
            "ano": year,
            "fase": phase,
            "niveis": answer_url_levels
        }, 200

    except Exception as erro:
        return {"erro": f"Erro na busca de niveis por ano e fase: {erro}"}, 500


def nav_problems(year: str, phase: str, level: str):
    try:
        answer_url_problems: list = []

        if year not in json_data.keys():
            return ("Ano não encontrado", 404)
        
        elif phase not in json_data[year].keys():
            return ("Fase não encontrada", 404)
        
        elif level not in json_data[year][phase].keys():
            return ("Nível não encontrado", 404)

        for problem in json_data[year][phase][level].keys():
            answer_url_problems.append(problem)

        return {
            "ano": year,
            "fase": phase,
            "nivel": level,
            "questoes": answer_url_problems
        }, 200

    except Exception as erro:
        return {"erro": f"Erro na busca de questões por ano, fase e nivel: {erro}"}, 500

def nav_problem(year: str, phase: str, level: str, problem: str): # O atributo nameProblem é um atributo identicado de questão temporario, caso no futuro queiramos usar ID
    try:
        specific_problem = None

        for problem in json_data[year][phase][level].keys():
            if problem == problem:
                specific_problem = json_data[year][phase][level][problem]

        if specific_problem is None:
            return {"error": "Questão não encontrada"}, 404
        else:
            return {
                "ano": year,
                "fase": phase,
                "nivel": level,
                "questao": specific_problem
            }, 200

    except Exception as erro:
        return {"erro": f"Erro na busca de questão específica por ano, fase, nivel e nome: {erro}"}, 500