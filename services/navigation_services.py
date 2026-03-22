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
    ...
    # {
    #   "ano": "2022",
    #   "fase": "1",
    #   "níveis": ["j", "1", "2", "s"]
    # }

def nav_problems(year: str, phase: str, level: str):
    ...
    # {
    #   "ano": "2022",
    #   "fase": "1",
    #   "nivel": "1",
    #   "questoes": ["nome", "otonome", "kaio", "AAAAAAAAAAAAAAAA"]
    # }
