import os
import pandas
import click
from pymongo import MongoClient, ASCENDING
import logging


@click.command()
@click.option("--srt_dir", "-i", "srt_dir", required=True)
@click.option("--srt_db", "-o", "mongo_server_string", required=True)
@click.option("--verbose", "-v", "verbose", is_flag=True, default=False)
def index_to_db(srt_dir, mongo_server_string, verbose):

    logging.basicConfig()
    logger = logging.getLogger("srt_indexer")
    if verbose is True:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    client = MongoClient(mongo_server_string)
    db = client.srt_db
    srt_collection = db.srt
    srt_collection.create_index([("media_path", ASCENDING), ("start_time", ASCENDING)], unique=True)

    docs_count = srt_collection.count()

    for file in os.listdir(srt_dir):

        if file.endswith(".csv"):
            file_path = os.path.join(srt_dir, file)
            df = pandas.read_csv(file_path)

            subs_data = df.to_dict(orient='records')
            # Add media_id to uniquely identify each row through-out the media
            for data in subs_data:
                data["media_path"] = file_path

            for data in subs_data:
                try:
                    resp = srt_collection.insert_one(data)
                except Exception as e:
                    logger.debug(e)

    updated_docs_count = srt_collection.count()
    logger.info(
        f'Added {updated_docs_count - docs_count} new dialogues to srt_db')
    client.close()


if __name__ == "__main__":
    index_to_db()
