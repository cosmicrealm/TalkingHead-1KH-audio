dataset=$1

python videos_download.py --input_list data_list/${dataset}_video_ids.txt --output_dir ${dataset}/raw_videos
python videos_split.py ${dataset}/raw_videos ${dataset}/1min_clips
python videos_crop_opencv.py --input_dir ${dataset}/1min_clips/ --output_dir ${dataset}/cropped_clips --clip_info_file data_list/${dataset}_video_tubes.txt