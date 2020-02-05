import connection
from flask import request, make_response, jsonify


def get_matches(string):
    '''
    Queries `srt_collection` for given `string` and returns most relevant matches
    '''

    with connection.SubtitlesDB() as srt_collection:
        # Not reusing a connection sucks real hard! Avoid

        results = srt_collection.find(
            {"$text": {"$search": string}},
            {"score": {"$meta": "textScore"}}
        )
        sorted_results = sorted(
            results,
            key=lambda match: match.get("score"),
            reverse=True
        )

        for match in sorted_results:
            del match["_id"]
            del match["score"]

        return sorted_results


def search():
    search_string = request.json.get("query")

    if search_string is None or len(search_string) == 0:
        return make_response("Invalid query", 400)

    search_matches = get_matches(search_string)

    return jsonify(search_matches)
