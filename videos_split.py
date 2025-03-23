import os
import subprocess
import sys

def split_video(in_dir, out_dir, segment_time='00:01:00'):
    # 创建输出目录（如果不存在）
    os.makedirs(out_dir, exist_ok=True)

    # 遍历输入目录中的每个 MP4 文件
    for filename in os.listdir(in_dir):
        if filename.endswith('.mp4'):
            input_file = os.path.join(in_dir, filename)
            output_pattern = os.path.join(out_dir, f"{filename[:-4]}_%04d.mp4")
            
            # 使用 ffmpeg 命令进行视频分割
            command = [
                'ffmpeg',
                '-i', input_file,
                '-c', 'copy',
                '-map', '0',
                '-segment_time', segment_time,
                '-f', 'segment',
                output_pattern
            ]
            
            try:
                subprocess.run(command, check=True)
                print(f"成功处理文件: {filename}")
            except subprocess.CalledProcessError as e:
                print(f"处理文件 {filename} 时出错: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python split_videos.py <输入目录> <输出目录>")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    split_video(input_directory, output_directory)
