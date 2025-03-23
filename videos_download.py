import argparse
import multiprocessing as mp
import os
from functools import partial
from time import time as timer
from func_yt_dlp import download_video_with_audio
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--input_list', type=str, required=True,
                    help='List of youtube video ids')
parser.add_argument('--output_dir', type=str, default='data/youtube_videos',
                    help='Location to download videos')
parser.add_argument('--num_workers', type=int, default=1,
                    help='How many multiprocessing workers?')
args = parser.parse_args()


def download_video(output_dir, video_id):
    r"""Download video."""
    video_path = '%s/%s.mp4' % (output_dir, video_id)
    if not os.path.isfile(video_path):
        try:
            # Download the highest quality mp4 stream.
            raw_url = 'https://www.youtube.com/watch?v=%s' % (video_id)
            save_name = os.path.join(output_dir, video_id + '.mp4')
            download_video_with_audio(raw_url, save_name)
        except Exception as e:
            print(e)
            print('Failed to download %s' % (video_id))
    else:
        print('File exists: %s' % (video_id))


if __name__ == '__main__':
    # Read list of videos.
    video_ids = []
    with open(args.input_list) as fin:
        for line in fin:
            video_ids.append(line.strip())

    # Create output folder.
    os.makedirs(args.output_dir, exist_ok=True)

    # Download videos.
    downloader = partial(download_video, args.output_dir)

    start = timer()
    pool_size = args.num_workers
    print('Using pool size of %d' % (pool_size))
    with mp.Pool(processes=pool_size) as p:
        _ = list(tqdm(p.imap_unordered(downloader, video_ids), total=len(video_ids)))
    print('Elapsed time: %.2f' % (timer() - start))
