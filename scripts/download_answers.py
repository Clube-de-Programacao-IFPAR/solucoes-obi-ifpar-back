import requests, re, json, zipfile, os.path
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint

# global to print errors at end of program
invalid_zips = {}

BASE_URL = "https://olimpiada.ic.unicamp.br"
VERSION = "0.1"
AGENT_NAME = f"ANSWER-LINK-DOWNLOADER/{VERSION}"

def get_filtered_urls(data):
    filtered = []
    for year in data.values():
        for phase in year.values():
            for naming_is_hard in phase.values():
                for url in naming_is_hard.values():
                    if not url[1]:
                        # url has not been downloaded, append to download later
                        filtered.append(url[0])
    
    return filtered

def update_urls(urls: list[str]): # updates to True
    with open("public/answer_urls.json") as file:
        answer_data = json.load(file)

    for url in urls:
        # more regex yeeeeeeeeeeeeeeee
        groups = re.search(r".+/(\d{4})(?:(c)f|f(\d))(b)?p([\djsu])_(.+).zip", url).groups()

        # group 1 is year
        # group 2 is c when is cfobi (competição feminina)
        # group 3 is normal phase
        # group 4 is b when it's split in A-B
        # group 5 is level of exam
        # group 6 is name of the question

        # will use this to put in the dict

        # as per specs in notion, [0] is url, [1] marks avaliability
        data = [url, True]

        answer_data[groups[0]][(groups[1] or "") + (groups[2] or "")][(groups[3] or "") + (groups[4] or "")][groups[5]] = data

    # dump all the urls back in the file
    with open("public/answer_urls.json", "w") as dump_file:
        json.dump(answer_data, dump_file, indent=2)


def download_zip(url: str, base_folder="public/answers/"):
    print(f"downloading zip from url {url}")
    # get zip name from the url to use as a folder name
    subfolder = re.search(r".+/(.+)\.zip", url).group(1)

    res = requests.get(BASE_URL + url, timeout=10, headers={"User-Agent": AGENT_NAME})

    if res.status_code != 200 and res.status_code != 201:
        invalid_zips[url] = f"ERROR {res.status_code}"
        print(f"Could not access zip from page {BASE_URL+url}, error: {res.status_code}")
        return False, url # silently fail as to not prevent other downloads from working


    zip_bytes = BytesIO(res.content)
    try:
        with zipfile.ZipFile(zip_bytes) as zip:
            zip.extractall(base_folder + subfolder)
    except zipfile.BadZipFile:
        invalid_zips[url] = "Bad Zip File"
        print(f"zip at {url} was invalid, skipping")
        return False, url
    
    # success?
    return True, url

def download_zips_parallel(urls: str, base_folder="public/answers/", max_workers=10):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_urls = {executor.submit(download_zip, url, base_folder): url for url in urls}

        for future in as_completed(future_to_urls):
            if future.result() and future.result()[0]:
                results.append(future.result()[1])
    
    return results

def main():
    with open("public/answer_urls.json") as file:
        answer_data = json.load(file)

    answer_urls = get_filtered_urls(answer_data)


    # download all the zips
    downloaded = download_zips_parallel(answer_urls)

    # update the urls file
    update_urls(downloaded)

    # pretty print all errors to stdout
    pprint(invalid_zips, indent=2)

if __name__ == "__main__":
    main()