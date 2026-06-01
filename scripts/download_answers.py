import requests, re, json, zipfile, os.path
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint

# global to print errors at end of program
invalid_zips = {}

BASE_URL = "https://olimpiada.ic.unicamp.br"
VERSION = "0.1"
AGENT_NAME = f"ANSWER-LINK-DOWNLOADER/{VERSION}"

def get_filtered_urls(data: dict[dict[dict[dict[dict]]]]):
    filtered = []
    folderNames = set()
    for year_key, year in data.items():
        for phase_key, phase in year.items():
            for level_key, level in phase.items():
                level: dict = level
                for name, info in level.items():
                    if not info[1]:
                        folderName = f"{year_key}_{phase_key}_{name}"
                        if folderName in folderNames: 
                            filtered.append(((info[0], True), folderName))
                            continue
                        # url has not been downloaded, append to download later
                        filtered.append((info[0], folderName))
                        folderNames.add(folderName)
    
    return filtered

def update_urls(urls: list[str]): # updates to True
    with open("questions/answer_urls.json") as file:
        answer_data = json.load(file)

    def mark_flag_as_downloaded(object, target_url):
        if isinstance(object, dict):
            for value in object.values():
                if isinstance(value, list) and len(value) == 2 and value[0] == target_url:
                    value[1] = True
                else:
                    mark_flag_as_downloaded(value, target_url)

    for url in urls:
        # support either a string (downloaded zip url) or a (url, name) pair
        if isinstance(url, (list, tuple)) and len(url) > 0:
            target = url[0]
        else:
            target = url

        mark_flag_as_downloaded(answer_data, target)

    # dump all the urls back in the file
    with open("questions/answer_urls.json", "w") as dump_file:
        json.dump(answer_data, dump_file, indent=2)


def download_zip(url: list[str, str], base_folder="questions/answers/"):
    zip_url, name = url[0], url[1]
    
    if isinstance(zip_url, (tuple, list)):
        return True, zip_url
    
    print(f"downloading zip from url {url}")
    # get zip name from the url to use as a folder name
    subfolder = name

    res = requests.get(BASE_URL + zip_url, timeout=10, headers={"User-Agent": AGENT_NAME})

    if res.status_code != 200 and res.status_code != 201:
        invalid_zips[zip_url] = f"ERROR {res.status_code}"
        print(f"Could not access zip from page {BASE_URL+zip_url}, error: {res.status_code}")
        return False, zip_url # silently fail as to not prevent other downloads from working


    zip_bytes = BytesIO(res.content)
    try:
        with zipfile.ZipFile(zip_bytes) as zip:
            for info in zip.infolist():
                # validate file names to avoid names like "../../path" or absolute paths
                # allow normal filenames with dots and directories, but reject traversal/absolute
                name = info.filename
                # normalize separators
                name_norm = name.replace("\\", "/")

                # skip directory entries
                if name_norm.endswith("/"):
                    continue

                if name_norm.startswith("/") or os.path.isabs(name) or any(part == ".." for part in name_norm.split("/")):
                    invalid_zips[zip_url] = f"Bad File Name {name}"
                    print(f"zip at {zip_url} contained invalid file name \"{name}\", skipping")
                    return False, zip_url
            zip.extractall(base_folder + subfolder)
    except zipfile.BadZipFile:
        invalid_zips[zip_url] = "Bad Zip File"
        print(f"zip at {zip_url} was invalid, skipping")
        return False, zip_url
    except FileExistsError:
        return True, zip_url
    
    # success?
    return True, zip_url

def download_zips_parallel(urls: list[list[str, str]], base_folder="questions/answers/", max_workers=10):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_urls = {executor.submit(download_zip, url, base_folder): url for url in urls}

        for future in as_completed(future_to_urls):
            if future.result() and future.result()[0]:
                results.append(future.result()[1])
    
    return results

def main():
    with open("questions/answer_urls.json") as file:
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
