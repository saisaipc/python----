import os
from moviepy.editor import VideoFileClip
import subprocess
import ffmpeg
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

''' 
在上面的函数基础上，
添加一个逻辑缓存逻辑，
先检查在当前程序文件夹里有没有名为“时长缓存”的文本文件，
有的话就读取数据，没有就创建一个名为“时长缓存”的文本文件，
将directory获取到的视频文件的时长存放到文本文件里。
在每一次对视频文件进行时长检测时，
先查看文本文件里有没有数据，有的话就用文本文件里的，没有就执行检查时长的流程
'''

# 时长的缓存文件路径
CACHE_FILE = "时长缓存.txt"

# 使用 ffprobe 获取视频时长，单位为秒
def get_video_duration(filepath):
    try:
        ffprobe_path = r'D:\ffmpeg-7.1\ffmpeg-7.1-essentials_build\bin\ffprobe.exe'  # 更换为 ffprobe.exe 的路径
        result = subprocess.run(
            [ffprobe_path, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return float(result.stdout.strip()) if result.stdout.strip() else None
    except Exception as e:
        print(f"Error retrieving duration for {filepath}: {e}")
        return None

# 读取时长的缓存
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# 保存时长的缓存
def save_cache(cache_data):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=4)

# 获取文件列表并获取每个视频的时长
def get_files_list(directory):
    # 读取缓存数据
    cache_data = load_cache()
    fileList = []

    # 找到所有视频文件
    video_files = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(directory)
        for file in files if file.endswith(('.AVI','.mp4','.avi','.mkv','.MP4', '.MOV', '.mov', '.webm', '.m4v'))
    ]
    
    # 检查缓存是否有该文件的时长信息
    to_process_files = []
    for file_path in video_files:
        if file_path in cache_data:
            # 从缓存加载
            fileList.append({'path': file_path, 'time': cache_data[file_path]})
        else:
            # 未缓存的文件添加到处理队列
            to_process_files.append(file_path)
    
    # 使用多线程并行获取视频时长，针对未缓存的文件
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_video_duration, file): file for file in to_process_files}
        for future in as_completed(futures):
            file_path = futures[future]
            try:
                duration = future.result()
                fileList.append({'path': file_path, 'time': duration})
                # 更新缓存
                cache_data[file_path] = duration
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
    
    # 保存更新后的缓存
    save_cache(cache_data)
    return fileList



# 下面的函数不会查找子文件夹
def get_videos_list(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(('.mp4','.avi','.mkv')):
            files.append(filename)
    return files

if __name__ == "__main__":
    # folder_path = input("请输入文件夹地址：")
    folder_path = "D:\python小程序"
    fileList = get_files_list(folder_path)
    for file in fileList:
        print(file)
    print(len(fileList))