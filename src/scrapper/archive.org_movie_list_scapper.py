import lxml.html as lh
from io import StringIO
import json

with open("./data/archive.org_pub_domain_movies.html") as in_:
    movie_listing_html = in_.read()

movies = lh.parse(StringIO(movie_listing_html)).findall(".//div[@data-id]")
movie_ids = [m.get("data-id") for m in movies[1:]]  # First item is a placeholder

with open("./data/movie_ids.json", "w+") as out:
    json.dump(fp=out, obj=movie_ids)

