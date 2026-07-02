import json
import re
from pathlib import Path
from collections import defaultdict
from pprint import pprint
# Importando as funções do get_urls script 
try:
    from scripts import get_urls
except ModuleNotFoundError:
    import get_urls

JSON_PATH = Path("questions/answer_urls.json")

def load_existing_data() -> dict:
    #Carrega o JSON atual se ele existir, caso contrário retorna um dicionário vazio.
    if JSON_PATH.exists():
        try:
            with JSON_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Aviso: O arquivo JSON estava corrompido. Começando do zero.")
            return {}
    return {}

def select_new_years(json_years, web_scraped_years) -> dict:
    years = web_scraped_years.copy()
    for year in web_scraped_years:
        match = re.search(r"OBI(\d+)", year)
        if match.group(1) in json_years.keys():
            years.remove(f"/passadas/OBI{match.group(1)}/")

    return years


def merge_data(existing: dict, new_data: dict) -> dict:
    def tree():
        return defaultdict(tree)

    merged = tree()
    for year, phases in existing.items():
        for phase, levels in phases.items():
            for level, files in levels.items():
                for filename, data in files.items():
                    merged[year][phase][level][filename] = data
                    
    for year, phases in new_data.items():
        for phase, levels in phases.items():
            for level, files in levels.items():
                for filename, data in files.items():
                    merged[year][phase][level][filename] = data
                    
    return merged

def main():
    web_scraped_years = get_urls.get_links(r"/passadas/", re.compile(r"^/passadas/OBI.+")) 
    json_data = load_existing_data()

    years = select_new_years(json_years=json_data,web_scraped_years=web_scraped_years)
    pprint(f'Anos encontrados: {", ".join(years)}')


    # aproveitando a lógica de get_urls
    exams = get_urls.get_links_parallel(years, re.compile(r"^/passadas/OBI\d{4}.+programacao.+"))
    
    answer_urls = get_urls.get_zips_parallel(exams, re.compile(r".+\.zip"))

    new_parsed_data = get_urls.parse_urls(answer_urls)

    # Junta os dois Jsons em um só
    final_data = merge_data(json_data, new_parsed_data)
    
    with JSON_PATH.open("w") as dump_file:
        json.dump(final_data, dump_file, indent=2)

if __name__ == "__main__":
    main()