import json
import requests
import lxml.html as lh
from io import BytesIO
from tqdm import tqdm

with open("data/movie_ids.json") as in_:
    movie_ids = json.load(in_)

movies = []
for id_ in tqdm(movie_ids):
    movie_download_page = f"https://archive.org/download/{id_}/"
    files_dir_page = requests.get(movie_download_page)
    files = lh.parse(BytesIO(files_dir_page.content)).findall(".//table//a[@href]")
    file_urls = [f.get("href") for f in files]

    mp4_exists = any(file_.endswith(".mp4") for file_ in file_urls)
    srt_exists = any(file_.endswith(".srt") for file_ in file_urls)
    compressed_exists = any("512kb" in file_ for file_ in file_urls)

    if not (mp4_exists and srt_exists):
        continue  # Skip this movie

    movie_media = {}

    for file_ in file_urls:

        if file_.endswith(".mp4"):
            if compressed_exists:
                if "512kb" in file_:
                    movie_media["video"] = movie_download_page + file_
            else:
                movie_media["video"] = movie_download_page + file_

        if file_.endswith(".srt"):
            movie_media["srt"] = movie_download_page + file_

    movies.append(movie_media)

print(f"Collected download URLs for {len(movies)} public domain movies.")
with open("./data/movie_media_urls.json", "w+") as out:
    json.dump(obj=movies, fp=out)

