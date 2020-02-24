import os
import pandas
import click
import logging
import pymongo


class SubtitlesDB(object):
    '''
    Context man for establishing mongodb connection to work on `srt_collection`
    '''

    def __init__(self, mongo_server_string):

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


@click.command()
@click.option("--srt_dir", "-i", "srt_dir", required=True)
@click.option("--srt_db", "-o", "mongo_server_string", required=True)
@click.option("--verbose", "-v", "verbose", is_flag=True, default=False)
def index_to_db(srt_dir, mongo_server_string, verbose):

    # logging
    logging.basicConfig()
    logger = logging.getLogger("srt_indexer")
    if verbose is True:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    with SubtitlesDB(mongo_server_string) as srt_collection:

        docs_count = srt_collection.estimated_document_count()
        # Iterate through all subtitle files and add each sub frame as a row
        for file in os.listdir(srt_dir):

            if file.endswith(".csv"):
                file_path = os.path.join(srt_dir, file)
                df = pandas.read_csv(file_path)

                subs_data = df.to_dict(orient='records')
                # Add media_id to uniquely identify each row through-out the media
                for data in subs_data:
                    data["media_name"] = file[:-4]
                    data["media_path"] = file_path

                for data in subs_data:
                    try:
                        resp = srt_collection.insert_one(data)
                    except Exception as e:
                        logger.debug(e)

        updated_docs_count = srt_collection.estimated_document_count()

    logger.info(
        f'Added {updated_docs_count - docs_count} new dialogues to srt_db')


if __name__ == "__main__":
    index_to_db()
