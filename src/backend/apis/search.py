import connection
from flask import request, make_response, jsonify


def utime_to_seconds(ts):
    # TODO: Add smooth consumption logic here.
    # Ignore ms, <video/> doesn't support that
    ts = ts[:-4]
    hh, mm, ss = ts.split(":")

    seconds = 0
    seconds += int(hh) * 60 * 60
    seconds += int(mm) * 60
    seconds += int(ss)

    return seconds


def derive_video_object(match):

    media_title = f'{match["dialogue"]}'
    start_secs = utime_to_seconds(match["start_time"])
    end_secs = utime_to_seconds(match["end_time"])
    media_url_qpars = f'#{start_secs},{end_secs}'
    media_url_base = connection.gcs_url_template.format(
        path=match["media_name"])
    media_url = f'{media_url_base}/{media_url_qpars}'

    videoObject = {
        "title": media_title,
        "url": media_url
    }

    return videoObject


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
            match["videoObject"] = derive_video_object(match)
            del match["_id"]
            del match["score"]

        return sorted_results


def search():
    search_string = request.json.get("query")

    if search_string is None or len(search_string) == 0:
        response = make_response("Invalid query", 400)

        return response

    search_matches = get_matches(search_string)
    response = make_response(jsonify(search_matches))

    return response
