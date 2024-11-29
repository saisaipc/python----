import os

def getFileName(fodPath):
    fileList = []
    for root, dirs, files in os.walk(fodPath):
        for file in files:
            if file.endswith(('.zip', '.jpg','.mhtml')):
                continue
            file = os.path.join(root, file)
            fileList.append(file)
            # print(os.path.join(root, file))  //包含了目录的
    return fileList

def filesRename(files):
    for file in files:
        newFile = file + '.mhtml'
        os.rename(file,newFile)

if __name__ == "__main__":
    foldPath = r"E:\ALL of Games\The Last of Us Part I v1.1.0\学习补丁+修改器+完美全解锁存档+赠品\学习补丁\网页漫画\10.28"
    files = getFileName(foldPath)
    print(len(files))
    filesRename(files)