import re
import os
import pdb
import click
import pandas


@click.command()
@click.option("--in_dir", "-i", "in_dir", required=True)
@click.option("--out_dir", "-o", "out_dir", required=True)
def srt_to_csv(in_dir, out_dir):
    '''
    Recursively finds srt files in `in_dir` and writes csv for each file.
    Each subtitle will have three cols: `start_time`, `end_time`, `dialogue`
    '''

    newline_charset = "(\r\n|\r|\n)"
    timestamp = "\d{2}:\d{2}:\d{2},\d{3}"
    frame_duration = f'(?P<start_time>{timestamp})\s*-->\s*(?P<end_time>{timestamp})'
    multiline_dialogue = f'(?P<multiline_dialogue>(.+{newline_charset})+)'
    SRT_PATTERN = f'{frame_duration}{newline_charset}{multiline_dialogue}'

    for root, dirs, files in os.walk(in_dir):
        for file in dirs + files:
            if file.endswith(".srt"):

                file_path = os.path.join(root, file)
                with open(file_path) as in_:
                    srt_data = in_.read()

                df_dict = {
                    "start_time": [],
                    "end_time": [],
                    "dialogue": []
                }
                for match in re.finditer(SRT_PATTERN, srt_data, re.MULTILINE):
                    # pdb.set_trace()
                    df_dict["start_time"].append(match.group("start_time"))
                    df_dict["end_time"].append(match.group("end_time"))
                    df_dict["dialogue"].append(match.group("multiline_dialogue"))

                df = pandas.DataFrame(df_dict)
                frame_count, _ = df.shape

                assert frame_count > 10, \
                    f'{file_path} wasn\'t extracted; frame_count: {frame_count}'

                # pdb.set_trace()
                out_path = os.path.join(out_dir, file[:-4] + ".csv")
                df.to_csv(out_path, index=False)


if __name__ == "__main__":
    srt_to_csv()
