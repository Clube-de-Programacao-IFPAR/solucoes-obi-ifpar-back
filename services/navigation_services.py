import json
from ..errors.invalid_field import InvalidField
from ..errors.missing_field import MissingField
from ..errors.content_not_found import ContentNotFound

JSON_DATA = {}

def load_json():
    global JSON_DATA
    if JSON_DATA != {}:
        return
    try:
        with open("./questions/answer_urls.json", "r", encoding="utf-8") as json_file:
            JSON_DATA = json.load(json_file)
    except FileNotFoundError:
        raise FileNotFoundError("Missing url json file at 'src/questions/answer_urls.json', follow the README to fix")

def validate(year=None, phase=None, level=None, problem=None):
    if year:
        if not year.isdigit():
            raise InvalidField("Invalid year format")
        if year not in JSON_DATA:
            raise ContentNotFound("Year not found")

    if phase:
        if phase not in ("c", "1", "2", "3"):
            raise InvalidField("Invalid phase format")
        if phase not in JSON_DATA[year]:
            raise ContentNotFound("Phase not found")

    if level:
        if level not in ("j", "1", "2", "s", "u"):
            raise InvalidField("Invalid level format")
        if level not in JSON_DATA[year][phase]:
            raise ContentNotFound("Level not found")

    if problem:
        if problem not in JSON_DATA[year][phase][level]:
            raise ContentNotFound("Problem not found")

    return None

def nav_years() -> tuple[dict[str, str | list[str]], int]:
    answer_url_years = list(JSON_DATA.keys())

    return {"anos": answer_url_years}, 200

def nav_phases(year: str) -> tuple[dict[str, str | list[str]], int]:
    validate(year)
    
    answer_url_phases = list(JSON_DATA[year].keys())

    return {
        "ano": year,
        "fases": answer_url_phases
    }, 200

def nav_levels(year: str, phase: str) -> tuple[dict[str, str | list[str]], int]:
    validate(year, phase)

    answer_url_levels = list(JSON_DATA[year][phase].keys())

    return {
        "ano": year,
        "fase": phase,
        "niveis": answer_url_levels
    }, 200

def nav_problems(year: str, phase: str, level: str) -> tuple[dict[str, str | list[str]], int]:
    validate(year, phase, level)

    answer_url_problems = list(JSON_DATA[year][phase][level].keys())

    return {
        "ano": year,
        "fase": phase,
        "nivel": level,
        "questoes": answer_url_problems
    }, 200

def nav_problem(year: str, phase: str, level: str, problem: str) -> tuple[dict[str, str], int]:
    validate(year, phase, level, problem)
    
    load_json()

    problem_url, problem_flag = JSON_DATA[year][phase][level][problem]

    return {
        "ano": year,
        "fase": phase,
        "nivel": level,
        "questao": problem,
        "url": problem_url,
        "flag": problem_flag
    }, 200
