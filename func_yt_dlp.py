import yt_dlp
import os
from datetime import datetime

def select_best_format_with_audio(formats):
    # 筛选出包含视频和音频的最佳组合
    best_combination = {
        "video": None,
        "audio": None
    }
    # 筛选出最高分辨率的视频
    video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') == 'none']
    if video_formats:
        best_combination["video"] = max(video_formats, key=lambda f: (f.get('height', 0), f.get('tbr', 0)))

    # 筛选出音频
    audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
    if audio_formats:
        # 默认将 abr 为 None 的情况设置为 0，避免比较出错
        best_combination["audio"] = max(audio_formats, key=lambda f: f.get('abr', 0) or 0)

    return best_combination

def download_video_with_audio(url, output_path='./output.mp4'):
    with yt_dlp.YoutubeDL() as ydl:
        # 获取视频信息
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        
        # 获取最佳视频和音频组合
        best_combination = select_best_format_with_audio(formats)
        video_format = best_combination["video"]
        audio_format = best_combination["audio"]

        if not video_format or not audio_format:
            print("Error: No video or audio format found")
            format_both = "best" 
        else:
            format_both = f"{video_format['format_id']}+{audio_format['format_id']}"

        # 设置下载选项，指定视频和音频格式
        ydl_opts = {
            'format': format_both,  # 指定最佳组合
            'outtmpl': output_path,  # 输出路径
            'merge_output_format': 'mp4',  # 合并为 MP4 格式
        }

        # 创建输出目录
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            # 下载并合并视频和音频
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_with_opts:
                ydl_with_opts.download([url])
        except Exception as e:
            print(f"Download Error: {e}")
            


def extract_video_info_from_playlist(playlist_url):
    ydl_opts = {
        'extract_flat': True,  # 只提取视频链接，不下载
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        video_info = []
        for entry in info_dict['entries']:
            # 获取每个视频的链接和标题
            video_info.append({
                'url': entry['url'],
                'title': entry.get('title', 'No Title')  # 提取视频标题
            })
        return video_info

def extract_video_links_from_channel(channel_url):
    ydl_opts = {
        'extract_flat': True,  # 只提取视频链接
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel_url, download=False)
        video_urls = []
        for entry in info_dict.get('entries', []):  # 确保有'entries'键
            print(entry)  # 打印每个条目的内容
            if 'url' in entry:
                video_urls.append(entry['url'])
            else:
                print("Warning: 'url' key not found in entry")
        return video_urls

def search_video_urls(query):
    query = f"ytsearch:{query}"
    # Create yt-dlp object and set search options
    ydl_opts = {
        'quiet': True,  # Don't print detailed information
        'extract_flat': True,  # Don't download video, just get info
        'max_downloads': 5,  # Limit the number of results
    }
    # Create yt-dlp object
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Search using the query
        search_results = ydl.extract_info(query, download=False)
        # print(search_results)
        if 'entries' in search_results:
            # Extract video URLs from the search results
            video_urls = [video['url'] for video in search_results['entries']]
            print(f"Found {len(video_urls)} videos.")
            return video_urls
        else:
            print("No videos found for the given query.")
            return []


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    test_single_url = False
    if test_single_url:
        video_url = "https://www.youtube.com/shorts/o7ywaqKp9hg"  # 替换为目标视频 URL
        output_file = f"output_test/single_video/{timestamp}.mp4"
        download_video_with_audio(video_url, output_file)
    
    test_playlist_url = False
    if test_playlist_url:
        playlist_url = "https://www.youtube.com/playlist?list=PLL3OeXu8-o_nZnZoWXglealRA6nyH604_"
        output_playlist_root  = "output_test/playlist"
        video_info = extract_video_info_from_playlist(playlist_url)
        for info in video_info:
            url = info['url']
            title = info['title']
            cur_time_step = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            output_file = f"{output_playlist_root}/{cur_time_step}.mp4"
            download_video_with_audio(url, output_file)
    
    test_channels_url = True
    if test_channels_url:
        channel_name = "https://www.youtube.com/@%E8%B1%8C%E8%B1%86%E6%80%9D%E7%BB%B4-k1e/shorts"
        output_channel_root = "output_test/channel"
        video_urls = extract_video_links_from_channel(channel_name)
        for index,url in enumerate(video_urls):
            cur_time_step = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            output_file = f"{output_channel_root}/{cur_time_step}.mp4"
            print(f"Downloading video from {index}/{len(video_urls)},{url} to {output_file}")
            download_video_with_audio(url, output_file)
    
    test_specific_topic = False
    if test_specific_topic:
        topics = ["小lin说",]
        output_topic_root = "output_test/topic"
        for topic in topics:
            cur_time_step = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            output_file = f"{output_topic_root}/{topic}/{cur_time_step}.mp4"
            video_urls = search_video_urls(topic)
            for url in video_urls:
                print(f"Downloading video from {url} to {output_file}")
                # download_video_with_audio(url, output_file)
    