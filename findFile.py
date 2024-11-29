import os
import re

def find_files_with_name(directory, pattern):
    # 编译正则表达式以提高性能
    regex = re.compile(pattern)

    # 遍历目标目录及其子目录
    for root_dir, dir_names, file_names in os.walk(directory):
        for filename in file_names:
            if regex.search(filename):
                print(os.path.join(root_dir, filename))

# 请将下面的路径替换为你需要搜索的实际路径
target_directory = r"E:\ALL of Games\The Last of Us Part I v1.1.0\学习补丁+修改器+完美全解锁存档+赠品\学习补丁"
pattern = r'naimi'  # 正则表达式模式

find_files_with_name(target_directory, pattern)

