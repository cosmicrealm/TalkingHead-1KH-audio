import argparse
import multiprocessing as mp
import os
from functools import partial
from time import time as timer

import cv2
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, required=True,
                    help='目录，包含输入视频文件（例如 youtube 视频剪辑）。')
parser.add_argument('--clip_info_file', type=str, required=True,
                    help='包含剪辑信息的文件，每行格式为：video_name, H, W, S, E, L, T, R, B')
parser.add_argument('--output_dir', type=str, required=True,
                    help='保存输出视频的文件夹。')
parser.add_argument('--num_workers', type=int, default=1,
                    help='使用多少个多进程工作进程？')
args = parser.parse_args()


def trim_and_crop(input_dir, output_dir, clip_params):
    # 解析参数
    video_name, H, W, S, E, L, T, R, B = clip_params.strip().split(',')
    H, W, S, E, L, T, R, B = int(H), int(W), int(S), int(E), int(L), int(T), int(R), int(B)
    S += 1  # 从 1 开始计数，而不是 0
    output_filename = '{}_S{}_E{}_L{}_T{}_R{}_B{}_mute.mp4'.format(video_name, S, E, L, T, R, B)
    output_filepath = os.path.join(output_dir, output_filename)
    if os.path.exists(output_filepath):
        print('输出文件 {} 已存在，跳过'.format(output_filepath))
        return

    input_filepath = os.path.join(input_dir, video_name + '.mp4')
    if not os.path.exists(input_filepath):
        print('输入文件 {} 不存在，跳过'.format(input_filepath))
        return

    # 打开视频文件
    cap = cv2.VideoCapture(input_filepath)
    if not cap.isOpened():
        print("无法打开视频文件", input_filepath)
        return

    # 获取实际视频的分辨率和 fps
    orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 根据原始参考尺寸计算裁剪区域（注意：T、B、L、R 是相对于参考值 H, W 的比例位置）
    t = int(T / H * orig_h)
    b = int(B / H * orig_h)
    l = int(L / W * orig_w)
    r = int(R / W * orig_w)
    crop_width = r - l
    crop_height = b - t

    # 设置视频写入器（使用 mp4v 编码）
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_filepath, fourcc, fps, (crop_width, crop_height))

    # 定位到起始帧 S
    cap.set(cv2.CAP_PROP_POS_FRAMES, S)
    current_frame = S

    # 逐帧读取，直到 E 帧（包含 E 帧）
    while current_frame <= E:
        ret, frame = cap.read()
        if not ret:
            break
        # 裁剪图像
        cropped = frame[t:b, l:r]
        writer.write(cropped)
        current_frame += 1
    cap.release()
    writer.release()
    # 截取音频，从 S, E 之间的部分
    # ffmpeg -i input.mp4 -ss S -to E -c copy -an output.wav
    audio_output_filepath = os.path.join(os.path.dirname(output_filepath), os.path.basename(output_filepath).replace('.mp4', '.wav')).replace('\\', '/')
    start_time = S / fps
    end_time = E / fps
    cmd_extract_audio = 'ffmpeg -y -i "{}" -ss {} -to {} -vn -acodec pcm_s16le "{}"'.format(
        input_filepath, start_time, end_time, audio_output_filepath)
    os.system(cmd_extract_audio)
    # combine video and audio
    cmd_combine = 'ffmpeg -y -i "{}" -i "{}" -c:v libx264 -c:a aac -strict experimental "{}"'.format(
        output_filepath, audio_output_filepath, output_filepath.replace('_mute', ''))
    os.system(cmd_combine)
    os.remove(output_filepath)
    os.remove(audio_output_filepath)
    print('输出文件保存至', output_filepath)


if __name__ == '__main__':
    # 读取剪辑信息列表
    clip_info = []
    with open(args.clip_info_file) as fin:
        for line in fin:
            if line.strip():
                clip_info.append(line.strip())

    # 确保输出文件夹存在
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 多进程执行任务
    downloader = partial(trim_and_crop, args.input_dir, args.output_dir)

    start = timer()
    pool_size = args.num_workers
    print('使用进程池大小: {}'.format(pool_size))
    with mp.Pool(processes=pool_size) as p:
        list(tqdm(p.imap_unordered(downloader, clip_info), total=len(clip_info)))
    print('耗时: {:.2f} 秒'.format(timer() - start))
