from flask import Blueprint
from ..services.navigation_services import nav_years, nav_phases, nav_levels, nav_problems, nav_problem

nav_BP = Blueprint("nav", __name__, url_prefix="/nav")

@nav_BP.route("/years", methods=["GET"])
def get_years():
    try:
        data = nav_years()
        return data
    except Exception as erro:
        return {"erro": f"Erro na requisição busca de anos: {erro}"}

@nav_BP.route("/years/<string:year>/phases", methods=["GET"])
def get_phases(year: str):
    try:
        data = nav_phases(year) 
        return (data)
    except TypeError as erro:
        return {"erro": f"Tipo de parâmetro de consulta invalido: {erro}"}
    except Exception as erro:
        return {"erro": f"Erro na requisição de busca de fases por ano: {erro}"}

@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels", methods=["GET"])
def get_levels(year: str, phase: str):
    try:
        data = nav_levels(year, phase)
        return data
    except TypeError as erro:
        return {"erro": f"Tipo de parâmetro de consulta invalido: {erro}"}
    except Exception as erro:
        return {"erro": f"Erro requisição de busca de niveis por ano e fase: {erro}"}

@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels/<string:level>/problems", methods=["GET"])
def get_problems(year: str, phase: str, level: str):
    try:
        data = nav_problems(year, phase, level)
        return data
    except TypeError as erro:
        return {"erro": f"Tipo de parâmetro de consulta invalido: {erro}"}
    except Exception as erro:
        return {"erro": f"Erro na requisição de busca de questões por ano, fase e nivel: {erro}"}
    


@nav_BP.route("/years/<string:year>/phases/<string:phase>/levels/<string:level>/problems/<string:nameProblem>", methods=["GET"])
def get_specificProblem(year: str, phase: str, level: str, nameProblem: str):
    try:
        data = nav_problem(year, phase, level, nameProblem)
        return data
    except TypeError as erro:
        return {"erro": f"Tipo de parâmetro de consulta invalido: {erro}"}
    except Exception as erro:
        return {"erro": f"Erro na requisição de busca de questão específica por ano, fase, nivel e nome: {erro}"}
