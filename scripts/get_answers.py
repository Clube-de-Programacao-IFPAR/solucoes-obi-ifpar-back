import requests, re, json, zipfile, os.path
from bs4 import BeautifulSoup
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed


BASE_URL = "https://olimpiada.ic.unicamp.br"

def get_links(url: str, filter: re.Pattern = None):
    # get all links in the url relative to the obi website with an optional regex filter
    print(f"Getting from url: {url}")
    res = requests.get(BASE_URL + url, timeout=10)
    
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

def already_downloaded(url: str, base_folder="answer_zips/"):
    subfolder = re.search(r".+/(.+)\.zip", url).group(1)

    # search for a zip already at the folder
    if os.path.isdir(base_folder + subfolder):
        return False

    return True

def download_zip(url: str, base_folder="answer_zips/"):
    print(f"downloading zip from url {url}")
    # get zip name from the url to use as a folder name
    subfolder = re.search(r".+/(.+)\.zip", url).group(1)

    res = requests.get(BASE_URL + url)

    if res.status_code != 200 and res.status_code != 201:
        print(f"Could not access zip from page {BASE_URL+url}, error: {res.status_code}")
        return # silently fail as to not prevent other downloads from working


    zip_bytes = BytesIO(res.content)
    try:
        with zipfile.ZipFile(zip_bytes) as zip:
            zip.extractall(base_folder + subfolder)
    except zipfile.BadZipFile:
        print(f"zip at {url} was invalid, skipping")
    
    return subfolder

def donwload_zips_parallel(urls: str, base_folder="answer_zips/", max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_urls = {executor.submit(download_zip, url, base_folder): url for url in urls}

        for future in as_completed(future_to_urls):
            if future.result():
                print(f"Finished downloading to {future.result()}")

if __name__ == "__main__":
    # won't explain all the regex in here, just know they match the links needed
    years = get_links("/passadas/", re.compile(r"^/passadas/OBI.+"))

    exams = get_links_parallel(years, re.compile(r"^/passadas/OBI\d{4}.+programacao.+"))
    
    answer_urls = get_links_parallel(exams, re.compile(r".+\.zip"))

    # dump all the urls in a file to marvel at later
    with open("answer_urls.json", "w") as dump_file:
        json.dump(answer_urls, dump_file)
    
    answer_urls = filter(already_downloaded, answer_urls)

    # donwload all the zips
    donwload_zips_parallel(answer_urls)