import os

def get_files_list(directory):
    fileList = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.AVI','.mp4','.avi','.mkv','.MP4', '.MOV', '.mov', '.webm', '.m4v')):
                file = os.path.join(root, file)
                fileList.append(file)
            # print(os.path.join(root, file))  //包含了目录的
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
    folder_path = "D:\大三下"
    fileList = get_files_list(folder_path)
    for file in fileList:
        print(file)
    print(len(fileList))