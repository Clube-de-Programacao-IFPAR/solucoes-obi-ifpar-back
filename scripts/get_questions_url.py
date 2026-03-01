import requests, json
from bs4 import BeautifulSoup as soup

base_url = "https://olimpiada.ic.unicamp.br"
bot_name = "answer-sheet-scraper"
version = "0.2"

headers = {
    "User-Agent": f"{bot_name}/{version}"
}

print(headers)


def get_previous_obi_urls() -> list[str] | None:
    response = requests.get(base_url + "/passadas/")
    if response.status_code == 200:
        content = response.text
    else:
        print(f"Failed getting the previous obi urls \nerror code: {response.status_code}")
        return

    return [a['href'] for a in soup(content, "html.parser").find_all('a', href=True) if a['href'][-8:-5] == "OBI"]

def get_obi_phases(obi_link):
    response = requests.get(base_url + obi_link)
    if response.status_code == 200:
        content = response.text
    else:
        print(f"Failed getting the previous obi urls \nerror code: {response.status_code}")
        return

    print(f"processing data from : {base_url + obi_link}")
    
    return [a['href'] for a in soup(content, "html.parser").find_all('a', href=True) if a['href'].endswith("/programacao/") or  a['href'].endswith("/programacao/cadernos/")]

def get_zip_paths(result_page_link):
    response = requests.get(base_url + result_page_link)
    if response.status_code == 200:
        content = response.text
    else:
        print(f"Failed getting the previous obi urls \nerror code: {response.status_code}")
        return

    print(f"processing data from : {base_url + result_page_link}")

    return [a['href'] for a in soup(content, "html.parser").find_all('a', href=True) if a['href'].endswith(".zip")]


print("getting previous obis")
obis = get_previous_obi_urls()

print("getting result links from obis")
links = [get_obi_phases(obis[i]) for i in range(len(obis))]
print("mocking results, just getting from 2020")
#links = [#['/passadas/OBI1999/programacao/'],
#         #['/passadas/OBI2006/fase1/programacao/',
#         # '/passadas/OBI2006/fase2/programacao/'],
#         ['/passadas/OBI2020/fase2/programacao/',
#          '/passadas/OBI2020/fase3/programacao/']
#         ]


for link in links:
    print(link)

all_paths = []

max_stuff = 1000000000
count = 0
zip_paths = []
print("getting zip paths")
for obi in links:
    if count >= max_stuff: break
    print(f"getting zip paths from {obi}")
    for phase in obi:
        print(f"getting zip paths from {obi} phase {phase}")

        paths = get_zip_paths(phase)
        for path in paths:
            all_paths.append(path)
            print(f"Ano {path[33: 37]} fase {path[38]} nivel {path[40]} nome {path[42: -4]}")
            zip_paths.append(path)

    count += 1

print(count)

print(all_paths)
for path in all_paths:
            print(f"Ano {path[33: 37]} fase {path[38]} nivel {path[40]} nome {path[42: -4]}: {path}")
            zip_paths.append(path)

organized_path = {}

print(len(all_paths)) # 662

for path in all_paths:
    cur = organized_path
    if not cur:
        cur = dict()
    
    cur = organized_path.get(path[33: 37])
    if not cur:
        organized_path[path[33: 37]] = dict()
    
    cur = organized_path.get(path[33: 37]).get(path[38])
    if not cur:
        organized_path[path[33: 37]][path[38]] = dict()
    
    cur = organized_path.get(path[33: 37]).get(path[38]).get(path[40])
    if not cur:
        organized_path[path[33: 37]][path[38]][path[40]] = dict()
    
    organized_path[path[33: 37]][path[38]][path[40]][path[42: -4]] = path

with open("../public/questions_url.json", "w") as file:
  file.write(json.dumps(organized_path))