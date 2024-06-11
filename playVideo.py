import subprocess
import platform
import time
import getFileList
import os
import psutil

def play_video(filepath):
    # 使用默认的视频播放器打开视频文件
    os.system('start "" "%s"' % filepath)

    # 下面的是gpt写的，没试过
    # video_path = r"D:\大三下\校内实习\视频+  +\16.mp4"
    # try:
    #     os.startfile(video_path)
    # except FileNotFoundError:
    #     print("文件不存在")

    # 下面的语句无法播放路径中有特殊字符的
    # subprocess.Popen(["start", filepath], shell=True)
    """
    os.system：
    os.system 是一个简单的方法，它在调用系统 shell 来执行命令时非常有用。
    它会阻塞当前的 Python 进程，直到执行的命令完成并返回结果。
    可以执行简单的命令，但是不太适合执行需要更多控制或与命令行交互的任务。

    subprocess.Popen：
    subprocess.Popen 提供了更多的灵活性和控制，可以用来执行更复杂的系统命令。
    它不会阻塞当前的 Python 进程，允许你在执行命令的同时进行其他操作。
    可以设置多种参数来控制命令的执行环境，如工作目录、环境变量等。
    通常更推荐使用 subprocess.Popen 来替代 os.system，特别是在需要执行复杂命令或需要更多控制的情况下。
    在你的情况下，由于只需要启动默认的视频播放器来打开视频文件，使用 os.system 或 subprocess.Popen 都可以。
    不过，subprocess.Popen 通常被认为更好，因为它提供了更多的控制和灵活性
    """

    # if platform.system() == "Windows":
    #     # Windows 平台下使用 cmd 打开视频
    #     subprocess.Popen(["start", filepath], shell=True)
    # elif platform.system() == "Darwin":
    #     # macOS 平台下使用 open 命令打开视频
    #     subprocess.Popen(["open", filepath])
    # elif platform.system() == "Linux":
    #     # Linux 平台下使用 xdg-open 命令打开视频
    #     subprocess.Popen(["xdg-open", filepath])
    # else:
    #     print("Unsupported operating system")


def close_video_player(videoplayer_name , pid):
    video_player_pid = None  # 初始化为 None，以防止在未找到匹配进程时引用错误

    # 第一次调用本函数获取原来的pid
    if pid == None :
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == videoplayer_name:
                video_player_pid = process.info['pid']
                return video_player_pid
        return (f"第一次未找到名称为 {videoplayer_name} 的视频播放器进程pid")
    
    try:
        process = psutil.Process(pid)
        process.terminate()  # 关闭进程
        return f"视频已关闭pid:{pid}"
    except psutil.NoSuchProcess:
        return "指定PID的进程不存在"
    except Exception as e:
        return f"关闭进程时发生错误：{e}"
    # print("函数运行结束")

# old_path是指带目录的文件名，new_name是指不带目录的文件名
def rename_file(old_path, new_name):
    # directory = r"D:\大三下\python视频整理"
    # getFileList.get_files_list(directory)

    old_forename = os.path.basename(old_path)
    # 获取原视频的后缀名
    old_extension = os.path.splitext(old_path)[1]

    index = 1
    while os.path.exists(new_name + old_extension):
        # new——name有问题，无限循环
        # 解决了
        new_name = f"{new_name}_{index}"
        print("发现重名文件，将命名改为" + new_name + old_extension) 
    
    # 有后缀的视频名
    new_name1 = new_name + old_extension

    
    while True:
        try:
            # 获取文件所在目录
            directory = os.path.dirname(old_path)
            # 构造新文件的完整路径
            new_path = os.path.join(directory, new_name1)
            # 重命名文件
            os.rename(old_path, new_path) 
            return f"{old_forename}  已重命名为  {new_name1}"
        except FileNotFoundError:
            return "文件不存在"
        except PermissionError:
            print("没有权限重命名文件")
            time.sleep(3)
        except Exception as e:
            print(f"发生错误：{e}")
            time.sleep(3)

def is_file_closed(file_path):
    """
    检查文件是否已经关闭
    """
    return not os.path.exists(file_path)


if __name__ == "__main__":
    filepath = r"D:\大三下\python视频整理\3.mp4"  # 替换成你的视频文件路径
    # play_video(filepath)

    player_name = "PotPlayer"
    # player_name = "wmplayer.exe"
    # close_video_player(player_name)
    old_pid = None
    old_pid = close_video_player(player_name , old_pid)
    print(old_pid)
    time.sleep(5)
        # 返回的是提示时为str，返回的是pid时为int
    if len(str(old_pid)) > 10 :
        print("没找到")
    else:
        print(close_video_player(player_name , old_pid))

    # # 要重命名的文件的路径（包括文件名）
    # old_path = filepath

    # # 文件的新名称
    # new_name = r"2"

    # # 执行文件重命名
    # tip = rename_file(old_path, new_name)
    # print(tip)
