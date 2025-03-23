# unittests for the scripts
python videos_download.py --input_list data_list/small_video_ids.txt --output_dir small/raw_videos
python videos_split.py small/raw_videos small/1min_clips
python videos_crop_opencv.py --input_dir small/1min_clips/ --output_dir small/cropped_clips --clip_info_file data_list/small_video_tubes.txt

# val for the scripts
python videos_download.py --input_list data_list/val_video_ids.txt --output_dir val/raw_videos
python videos_split.py val/raw_videos val/1min_clips
python videos_crop_opencv.py --input_dir val/1min_clips/ --output_dir val/cropped_clips --clip_info_file data_list/val_video_tubes.txt

# train for the scripts
python videos_download.py --input_list data_list/train_video_ids.txt --output_dir train/raw_videos
python videos_split.py train/raw_videos train/1min_clips
python videos_crop_opencv.py --input_dir train/1min_clips/ --output_dir train/cropped_clips --clip_info_file data_list/train_video_tubes.txt