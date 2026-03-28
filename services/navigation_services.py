import json

with open("./public/answer_urls.json", "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

def nav_years():
    try:
        answer_url_years = []
        for year in json_data.keys():
            answer_url_years.append(year)

        result: dict = { "anos": answer_url_years }

        return result
    
    except Exception as erro:
        return {"erro": f"Erro na busca de anos: {erro}"}
    

def nav_phases(year: str): 
    try:
        answer_url_phases: list = []

        if year not in json_data.keys():
            return ("Ano não encontrado", 404)
        
        for phase in json_data[year].keys():
            answer_url_phases.append(phase)

        result: dict = {
            "ano": year,
            "phases": answer_url_phases
        }

        return result
    
    except TypeError as erro:
        return {"erro": f"Tipo de parâmetro de consulta invalido: {erro}"}
    except Exception as erro:
        return {"erro": f"Erro na busca de fases por ano: {erro}"}


def nav_levels(year: str, phase: str):
    try:
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
            "niveis": answer_url_levels
        }

        return result
    
    except TypeError as erro:
        return {"erro": f"Tipo de parâmetro de consulta invalido: {erro}"}
    
    except Exception as erro:
        return {"erro": f"Erro na busca de niveis por ano e fase: {erro}"}


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

        result: dict = {
            "ano": year,
            "fase": phase,
            "nivel": level,
            "questoes": answer_url_problems
        }

        return result
    
    except TypeError as erro:
        return {"erro": f"Tipo de parâmetro de consulta invalido: {erro}"}
    except Exception as erro:
        return {"erro": f"Erro na busca de questões por ano, fase e nivel: {erro}"}


def nav_problem(year: str, phase: str, level: str, nameProblem: str): # O atributo nameProblem é um atributo identicado de questão temporario, caso no futuro queiramos usar ID
    try:
        specific_problem = None

        for problem in json_data[year][phase][level].keys():
            if problem == nameProblem:
                specific_problem = json_data[year][phase][level][nameProblem]

        if specific_problem is None:
            return ("Questão não encontrada", 404)
        else:
            result: dict = {
                "ano": year,
                "fase": phase,
                "nivel": level,
                "questao": specific_problem
            }

            return result
        
    except TypeError as erro:
        return {"erro": f"Tipo de parâmetro de consulta invalido: {erro}"}
    except Exception as erro:
        return {"erro": f"Erro na busca de questão específica por ano, fase, nivel e nome: {erro}"}