# Improvements on TalkingHead-1KH Video Download and Processing

## Introduction

Due to environmental issues, downloading the TalkingHead-1KH dataset using pytube results in errors, and the downloaded audio files are empty. To address this, I modified the original code by **replacing pytube with yt-dlp for video downloading**, and **used opencv and ffmpeg to reimplement the video editing and audio extraction processes**.

Original repository reference:  [TalkingHead-1KH](https://github.com/tcwang0509/TalkingHead-1KH)

## Key Modifications

- Video Download: Replaced pytube with yt-dlp for better compatibility and stability.

- Video Editing: Utilized opencv for video processing to enhance efficiency.

- Audio Extraction: Used ffmpeg to extract audio, ensuring completeness and usability.

## Example Downloaded Videos in Val

https://github.com/user-attachments/assets/09e87826-8e56-49c8-8a16-1a2a1b06cdb2

https://github.com/user-attachments/assets/06c11201-c359-41dd-9442-cd2d3d0525f5

https://github.com/user-attachments/assets/cb02a8ac-b0f5-4c40-8d7a-3f646249a572

https://github.com/user-attachments/assets/e7af37ec-a111-468d-ae08-32df7edb7a0e



ffmpeg -i samples/1lSejjfNHpw_0075_S1_E728_L671_T47_R1471_B847.mp4 -c:v libx264 -c:a aac -strict experimental -movflags +faststart 1lSejjfNHpw_0075_S1_E728_L671_T47_R1471_B847.mp4

ffmpeg -i samples/85UEFVcmIjI_0014_S93_E627_L558_T134_R1294_B870.mp4 -c:v libx264 -c:a aac -strict experimental -movflags +faststart 85UEFVcmIjI_0014_S93_E627_L558_T134_R1294_B870.mp4


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

Due to the limitations of video availability and YouTube's IP restrictions, I may share the processed dataset with attached audio at a later time.

## Acknowledgment

Special thanks to the [TalkingHead-1KH](https://github.com/tcwang0509/TalkingHead-1KH)
 Official Repository for providing the original implementation.

