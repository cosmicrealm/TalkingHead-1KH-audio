# TalkingHead-1KH-audio

## 🎉 Processed Dataset Available

The processed TalkingHead-1KH dataset **with audio** is now available on Hugging Face:

🤗 **[zhangjinyang/TalkingHead-1KH-audio](https://huggingface.co/datasets/zhangjinyang/TalkingHead-1KH-audio)**

You can directly download and use the processed dataset without running the processing scripts yourself.

---

## Introduction

Due to environmental issues, downloading the TalkingHead-1KH dataset using pytube results in errors, and the downloaded audio files are empty. To address this, I modified the original code by **replacing pytube with yt-dlp for video downloading**, and **used opencv and ffmpeg to reimplement the video editing and audio extraction processes**.

Original repository reference: [TalkingHead-1KH](https://github.com/tcwang0509/TalkingHead-1KH)

## Key Modifications

- **Video Download**: Replaced pytube with yt-dlp for better compatibility and stability.
- **Video Editing**: Utilized opencv for video processing to enhance efficiency.
- **Audio Extraction**: Used ffmpeg to extract audio, ensuring completeness and usability.

## Project Structure

```
├── func_yt_dlp.py          # yt-dlp wrapper for downloading YouTube videos
├── videos_download.py      # Download videos from YouTube by video IDs
├── videos_split.py         # Split long videos into 1-minute clips
├── videos_crop.py          # Crop videos using ffmpeg (alternative method)
├── videos_crop_opencv.py   # Crop videos and extract audio using OpenCV + ffmpeg
├── run_scripts.sh          # Main script to run the full pipeline
├── run_scripts_manual.sh   # Manual step-by-step commands
└── data_list/              # Video IDs and tube information files
```

## Example Downloaded Videos in Val

https://github.com/user-attachments/assets/09e87826-8e56-49c8-8a16-1a2a1b06cdb2

https://github.com/user-attachments/assets/06c11201-c359-41dd-9442-cd2d3d0525f5

https://github.com/user-attachments/assets/cb02a8ac-b0f5-4c40-8d7a-3f646249a572


## Dependency Installation

Make sure the following dependencies are installed in your environment:

```bash
pip install yt-dlp opencv-python ffmpeg-python tqdm
```

Additionally, ensure that **ffmpeg** is installed on your system:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows (using chocolatey)
choco install ffmpeg
```

## Usage

### Option 1: Use Pre-processed Dataset (Recommended)

Download the processed dataset directly from Hugging Face:

```python
from datasets import load_dataset

dataset = load_dataset("zhangjinyang/TalkingHead-1KH-audio")
```

Or download manually from: https://huggingface.co/datasets/zhangjinyang/TalkingHead-1KH-audio

### Option 2: Process Dataset Yourself

Run scripts for video downloading, video clipping, video cropping, and audio extraction:

```bash
# Unittests for the scripts (small subset)
bash run_scripts.sh small

# Validation set
bash run_scripts.sh val

# Training set
bash run_scripts.sh train
```

### Pipeline Details

The processing pipeline consists of three main steps:

1. **Download Videos**: Download raw videos from YouTube using yt-dlp
   ```bash
   python videos_download.py --input_list data_list/${dataset}_video_ids.txt --output_dir ${dataset}/raw_videos
   ```

2. **Split Videos**: Split long videos into 1-minute clips
   ```bash
   python videos_split.py ${dataset}/raw_videos ${dataset}/1min_clips
   ```

3. **Crop & Extract Audio**: Crop face regions and extract corresponding audio
   ```bash
   python videos_crop_opencv.py --input_dir ${dataset}/1min_clips/ --output_dir ${dataset}/cropped_clips --clip_info_file data_list/${dataset}_video_tubes.txt
   ```

## Acknowledgment

Special thanks to the [TalkingHead-1KH](https://github.com/tcwang0509/TalkingHead-1KH) Official Repository for providing the original implementation.

## License

This project follows the original TalkingHead-1KH license. Please refer to the [LICENSE](LICENSE) file for details.

