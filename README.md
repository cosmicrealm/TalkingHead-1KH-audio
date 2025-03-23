# Improvements on TalkingHead-1KH Video Download and Processing

## Introduction

Due to environmental issues, downloading the TalkingHead-1KH dataset using pytube results in errors, and the downloaded audio files are empty. To address this, I modified the original code by replacing pytube with yt-dlp for video downloading, and used opencv and ffmpeg to reimplement the video editing and audio extraction processes.

Original repository reference:  [TalkingHead-1KH](https://github.com/tcwang0509/TalkingHead-1KH)

## Key Modifications

- Video Download: Replaced pytube with yt-dlp for better compatibility and stability.

- Video Editing: Utilized opencv for video processing to enhance efficiency.

- Audio Extraction: Used ffmpeg to extract audio, ensuring completeness and usability.

## Dependency Installation

Make sure the following dependencies are installed in your environment:
```
pip install yt-dlp opencv-python ffmpeg-python
```

Additionally, ensure that ffmpeg is installed on your system. 

## Usage
Run scripts for video downloading, video clipping, video cropping, and audio extraction.
```
# Unittests for the scripts
bash run_scripts.sh small

# Validation for the scripts
bash run_scripts.sh val

# Training for the scripts
bash run_scripts.sh train

```

## Future Plans

I may share the processed dataset with attached audio at a later time.

## Acknowledgment

Special thanks to the [TalkingHead-1KH](https://github.com/tcwang0509/TalkingHead-1KH)
 Official Repository for providing the original implementation.

