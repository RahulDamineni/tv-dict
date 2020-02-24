import pymongo

default_connection = "mongodb://localhost:27017/"
gcs_url_template = "https://storage.googleapis.com/storage-tvdict/{path}.mp4"


class SubtitlesDB(object):

    def __init__(self, mongo_server_string=default_connection):

        # Getting to the right collection in Mongo server
        self.client = pymongo.MongoClient(mongo_server_string)
        db = self.client.srt_db
        self.srt_collection = db.srt

        # Uniquely id each dialogue identifiable across all media in DB
        self.srt_collection.create_index([
            ("media_path", pymongo.ASCENDING),
            ("start_time", pymongo.ASCENDING)],
            unique=True)

        # Make text content searchable
        self.srt_collection.create_index([("dialogue", "text")])

    def __enter__(self):
        return self.srt_collection

    def __exit__(self, type, value, traceback):
        self.client.close()
