import requests, re, json
from bs4 import BeautifulSoup, Tag
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from pathlib import Path

BASE_URL = "https://olimpiada.ic.unicamp.br"
VERSION = "0.1"
AGENT_NAME = f"ANSWER-LINK_SCRAPE/{VERSION}"

def get_links(url: str, filter: re.Pattern = None):
    # get all links in the url relative to the obi website with an optional regex filter
    print(f"Getting from url: {url}")
    res = requests.get(BASE_URL + url, timeout=10, headers={"User-Agent": AGENT_NAME})
    
    if res.status_code != 200 and res.status_code != 201:
        print(f"Could not get links from page {BASE_URL+url}, error: {res.status_code}")
        return [] # silently fail as to not halt the entire program
        
    document = BeautifulSoup(res.text, "html.parser")

    links = document.find_all("a")
    if filter:
        filtered_links = []
        for link in links:
            filtered = filter.match(link.attrs["href"])
            if filtered != None:
                filtered_links.append(filtered.string)
    
        return filtered_links
    return links

def get_links_parallel(urls: list[str], filter: re.Pattern=None, max_workers=10):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_urls = {executor.submit(get_links, url, filter): url for url in urls}

        for future in as_completed(future_to_urls):
            results.extend(future.result())
    
    return results

def get_zips(url: str, filter: re.Pattern = None):
    print(f"Getting from url: {url}")
    res = requests.get(BASE_URL + url, timeout=10, headers={"User-Agent": AGENT_NAME})
    
    if res.status_code != 200 and res.status_code != 201:
        print(f"Could not get links from page {BASE_URL+url}, error: {res.status_code}")
        return [] # silently fail as to not halt the entire program
        
    document = BeautifulSoup(res.text, "html.parser")

    return parse_zips(document, filter)

def get_zips_parallel(urls: list[str], filter: re.Pattern=None, max_workers=10):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_urls = {executor.submit(get_zips, url, filter): url for url in urls}

        for future in as_completed(future_to_urls):
            results.extend(future.result())
    
    return results

def parse_zips(document: BeautifulSoup, filter: re.Pattern = None) -> dict:
    links: list[Tag] = document.find_all("a")
    
    res = []
    
    for link in links:
        if filter is not None and not filter.match(link.attrs["href"]): continue
        title = link.find_previous("h4")
        if title is None or not re.match(r"Nível.+", title.get_text()):
            title = link.find_previous("h3")
        if title is None or not re.match(r"Nível.+", title.get_text()):
            title = link.find_previous("h2")
        if title is None or not re.match(r"Nível.+", title.get_text()):
            title = link.find_previous("h1")
        if title is None or not re.match(r"Nível.+", title.get_text()):
            title = None
        
        
        
        if title is None: title = ""
        else: title = title.get_text()
        
        pmatch = re.match(re.compile(r"/static/extras/obi(\d{4})/.*?(cf|f\d+)", re.IGNORECASE), link.attrs["href"])
        
        year = pmatch.group(1)
        phase = pmatch.group(2)
        
        if phase[0] == "f": phase = phase[1]
        
        res.append({
            "link": link.attrs["href"],
            "level": convert_level(title),
            "phase": phase,
            "year": year
        })
    
    return res

def convert_level(level: str) -> str:
    level = level.strip().lower()

    patterns = [
        (r"^nível\s*s.*$", "s"),
        (r"^nível\s*j.*$", "j"),
        (r"^nível\s*u.*$", "u"),
        (r"^nível\s*1$", "1"),
        (r"^nível\s*2$", "2"),
        (r"^nível\s*3$", "3"),
    ]

    for pattern, result in patterns:
        if re.match(pattern, level, re.IGNORECASE):
            return result

    return ""

def parse_urls(urls: list[dict]):
    def tree(): # on no value the dict creates a new dict
        return defaultdict(tree)

    parsed = tree()
    
    urls = sorted(urls, key=lambda url: (url["year"], url["phase"], url["level"]))
    
    for link in urls:
        data = [link["link"], False]
        
        name = re.match(re.compile(r".+_(.+)\.zip"), link["link"]).group(1)

        parsed[link["year"]][link["phase"]][link["level"]][name] = data
    
    return parsed

def main():
    # won't explain all the regex in here, just know they match the links needed
    years = get_links("/passadas/", re.compile(r"^/passadas/OBI.+"))

    exams = get_links_parallel(years, re.compile(r"^/passadas/OBI\d{4}.+programacao.+"))
    
    answer_urls = get_zips_parallel(exams, re.compile(r".+\.zip"))

    output_path = Path("questions/answer_urls.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # dump all the urls in a file
    with output_path.open("w") as dump_file:
        json.dump(parse_urls(answer_urls), dump_file, indent=2)
        
if __name__ == "__main__":
    main()
