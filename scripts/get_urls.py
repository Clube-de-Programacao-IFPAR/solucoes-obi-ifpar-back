import requests, re, json
from bs4 import BeautifulSoup
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

def parse_urls(urls: list[str]):
    # sort the urls cuz the threading messess up the order
    urls = sorted(urls)
    def tree(): # on no value the dict creates a new dict
        return defaultdict(tree)

    parsed = tree()

    for url in urls:
        # more regex yeeeeeeeeeeeeeeee
        groups = re.search(r".+/(\d{4})(?:(cf)|f(\d))(b)?p([\djsu])_(.+).zip", url).groups()

        # group 1 is year
        # group 2 is c when is cfobi (competição feminina)
        # group 3 is normal phase
        # group 4 is b when it's split in A-B
        # group 5 is level of exam
        # group 6 is name of the question

        # will use this to put in the dict

        # as per specs in notion, [0] is url, [1] marks avaliability
        data = [url, False]

        parsed[groups[0]][(groups[1] or "") + (groups[2] or "")][(groups[3] or "") + (groups[4] or "")][groups[5]] = data

    return parsed

def main():
    # won't explain all the regex in here, just know they match the links needed
    years = get_links("/passadas/", re.compile(r"^/passadas/OBI.+"))

    exams = get_links_parallel(years, re.compile(r"^/passadas/OBI\d{4}.+programacao.+"))
    
    answer_urls = get_links_parallel(exams, re.compile(r".+\.zip"))

    output_path = Path("questions/answer_urls.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # dump all the urls in a file
    with output_path.open("w") as dump_file:
        json.dump(parse_urls(answer_urls), dump_file, indent=2)
        
if __name__ == "__main__":
    main()