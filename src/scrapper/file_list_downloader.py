import os
import json
from tqdm import tqdm

with open("./data/movie_media_urls.json") as in_:
    movies = json.load(in_)


for m in tqdm(movies):
    os.system(f"wget {m['video']} -P data/videos")
    os.system(f"wget {m['srt']} -P data/subtitles")
