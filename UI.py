# python路径：C:/Users/Windows/AppData/Local/Microsoft/WindowsApps/python3.11.exe
# 本项目使用的是 PotPlayer 播放器
import tkinter as tk
import getFileList 
import playVideo
import time
import os
from tkinter import ttk
from tkinter import messagebox
import json

# 在文件开头添加配置变量
POTPLAYER_PATH = r"D:\PotPlayer\PotPlayerMini64.exe"  # 可以根据实际安装路径修改
DEFAULT_VIDEO_FOLDER = r"E:\ALL of Games\The Last of Us Part I v1.1.0\学习补丁+修改器+完美全解锁存档+赠品\学习补丁"

# TODO 关键词查询时的数量可以变一变

# 全局变量，用于存储当前视频列表
# 在函数中用globle表示使用的是全局变量，函数中不能使用同名的变量
# 视频目录列表
video_list = []

# 用于存储视频文件的路径，时长信息
videofiles_list = []

# 全局变量，用于存储点击次数
click_count = 0

# folder_path = r"D:\python小程序\python视频整理"
folder_path = DEFAULT_VIDEO_FOLDER

video_player = "wmplayer.exe"
video_player = POTPLAYER_PATH

# 双击列表项事件处理函数
def on_listbox_double_click(event):
    global click_count
    click_count += 1
    if click_count == 3:
        # 获取双击选中的项目索引
        index = listbox.curselection()
        if index:
            video_path = listbox_box.get(index[0])
            playVideo.play_video(video_path)
        click_count = 0
    elif click_count == 2:
        # 原来的双击功能
        index = listbox.curselection()
        if index:
            # 获取选中的项目内容
            selected_item = listbox.get(index)
            selected_item_box = listbox_box.get(index) # box里的全部是有目录的
            entry_box.delete(0, tk.END)  # 清空 entry_box 中的内容
            entry_box.insert(0, selected_item_box)  # 插入选中的项目内容
            # 将选中的项目显示在 Entry 中
            entry.delete(0, tk.END)  # 清空 Entry 中的内容
            entry.insert(0, selected_item)

# 播放下一个视频
def button_play_next1():
    global video_player
    index = listbox.curselection()
    if index:
        index = (index[0] + 1,)
        # 获取选中的项目内容
        selected_item = listbox.get(index)
        selected_item_box = listbox_box.get(index)
        entry_box.delete(0, tk.END)  # 清空 Entry 中的内容?
        entry_box.insert(0, selected_item_box)  # 插入选中的项��内容
        # 将选中的项目显示在 Entry 中
        entry.delete(0, tk.END)  # 清空 Entry 中的内容
        entry.insert(0, os.path.basename(selected_item))  # 插入选中的项目内容
        
        pid = None
        old_pid = playVideo.close_video_player(video_player , pid)
        # 返回的是提示时为str，返回的是pid时为int
        if len(str(old_pid)) > 10 :
            entry_tip_updata(f"没有查询到{video_player}")
            return
        # t = threading.Thread(target = button_play_video1)
        # t.start()
        # t.join()
        button_play_video1()
        print(old_pid)
        msg = playVideo.close_video_player(video_player , old_pid)
        entry_tip_updata(msg)
        
# 播放视频 //可以在这里就获取pid
def button_play_video1():
    safe_execute(
        lambda: playVideo.play_video(entry_box.get()),
        "播放视频失败"
    )

# 关闭视频
def button_close_video1():
    global video_player
    start_time = time.time()
    old_pid = playVideo.close_video_player(video_player)
    end_time = time.time()
    # print(f"第一次调用运行时间: {end_time - start_time:.6f} 秒")
    # 返回的是提示时为str，返回的是pid时为int
    if len(str(old_pid)) > 10 :
        entry_tip_updata(f"没有查询到{video_player}")
        return
    start_time = time.time()
    msg2 = playVideo.close_video_player(video_player , old_pid)
    end_time = time.time()
    # print(f"第二次调用运行时间: {end_time - start_time:.6f} 秒")
    entry_tip_updata(msg2)

# 改名按钮
def button_update_Name1():
    # 检测是否选择了视频文件
    oldname = entry_box.get()
    if oldname != "":
        newname = entry_update_Name.get()
        if newname != "" and newname != "输入名称":
            tip = playVideo.rename_file(oldname, newname, encoding='utf-8')  # 指定编码为 UTF-8
            entry_tip_updata(tip)
        else:
            entry_tip_updata("请输入名称！")
        return
    entry_tip_updata("请先输入改名文件的名称！")
    return

# 提示框
def entry_tip_updata(msg):
    Label_tip.config(text = msg)

# 过滤高于 U+FFFF 的 Unicode 字符
def filter_unicode(text):
    return ''.join(c if ord(c) <= 0xFFFF else '?' for c in text)

def format_duration(duration):
    """格式化时长显示"""
    if duration is None:
        return ""
    
    if duration < 60:  # 小于1分钟
        return f" [{int(duration)}秒]"
    elif duration < 3600:  # 1分钟到1小时
        minutes = duration / 60
        return f" [{minutes:.1f}分钟]"
    else:  # 1小时以上
        hours = duration / 3600
        return f" [{hours:.1f}小时]"

# 更新 Listbox 中添加项目
def button_update_list1():
    global video_list
    global folder_path
    global videofiles_list
    listbox.delete(0, tk.END)
    listbox_box.delete(0, tk.END)
    folder_from_entry = entry_folder.get()
    if folder_from_entry != "请输入视频目录地址..." and folder_from_entry != "":
        video_list = []
        folder_path = folder_from_entry
        videofiles_list = getFileList.get_files_list(folder_path)
        for item in videofiles_list:
            video_list.append(item['path'])
        entry_tip_updata(f"正使用输入的目录，共查询到 {len(video_list)} 个视频")
    else:
        video_list = []
        videofiles_list = getFileList.get_files_list(folder_path)
        for item in videofiles_list:
            video_list.append(item['path'])
        entry_tip_updata(f"正使用默认的目录，查询到 {len(video_list)} 个视频")
    # 默认按照文件名进行排序
    video_list.sort()
    for item in video_list:
        duration = next((file['time'] for file in videofiles_list if file['path'] == item), None)
        duration_str = format_duration(duration)
        listbox.insert(tk.END, filter_unicode(os.path.basename(item) + duration_str))
        listbox_box.insert(tk.END, filter_unicode(item))

# 输入地址框的绑定函数
def on_entry_click(event):
    if entry_folder.get() == '请输入视频目录地址...':
       entry_folder.delete(0, "end") # 删除现有内容
       entry_folder.insert(0, '') # 插入空字符
       entry_folder.config(fg = 'black') # 将字体颜色设置为黑色

def on_focus_out(event):
    if entry_folder.get() == '':
        entry_folder.insert(0, '请输入地址...')
        entry_folder.config(fg = 'grey') # 将字体颜色设置为灰色

# 搜索视频,按空格分割
def search_videos():
    if listbox.get(0) == "":
        entry_tip_updata("请先刷新列表！")
        return
        
    keywords = entry_search.get().strip().split()  # 获取搜索关键词，去除首尾空格并按空格分割
    keywords_len = len(keywords)
    if not keywords or entry_search.get() == "搜索框(关键词按空格分割)":
        entry_tip_updata("请先输入文字！")
        return

    # 重新获取当前目录下的视频列表
    folder_from_entry = entry_folder.get()
    if folder_from_entry != "请输入视频目录地址..." and folder_from_entry != "":
        current_folder = folder_from_entry
    else:
        current_folder = folder_path
        
    # 重新扫描目录获取最新的视列表
    global videofiles_list
    videofiles_list = getFileList.get_files_list(current_folder)
    global video_list
    video_list = [item['path'] for item in videofiles_list]

    # 计算每个视频文件名中包含的关键词数
    video_score = {}
    for video_path in video_list:
        # 检查文件是否存在
        if os.path.exists(video_path):
            video_name = os.path.basename(video_path)
            # 对每一个视频进行关键词查找
            score = sum(keyword.lower() in video_name.lower() for keyword in keywords)
            video_score[video_path] = score

    values_list = list(video_score.values())
    if not values_list:
        entry_tip_updata("没有查询到对应的视频！")
        return
    else:
        count_non_zero = sum(1 for element in values_list if element == keywords_len)
        entry_tip_updata(f"查询完成! 共有 {count_non_zero} 个视频")

    # 根据得分对视频列表进行排序
    video_list.sort(key=lambda x: -video_score.get(x, 0))
    after_search_video_list = list(filter(lambda x: video_score.get(x, 0) == keywords_len, video_list))

    # 更新列表框中的内容
    listbox.delete(0, tk.END)
    listbox_box.delete(0, tk.END)
    for video_path in after_search_video_list:
        listbox.insert(tk.END, os.path.basename(video_path))
        listbox_box.insert(tk.END, video_path)

"""
# 设置输入框的默认提示文本为“你好”
set_default_text(entry_tip, '你好')
"""
def set_default_text(entry, default_text):
    """
    设置输入框的默认提示文本，并绑定相关事件。

    参数:
    entry (tk.Entry): 要设置默认提示文本的输入框。
    default_text (str): 要显示的默认提示文本。
    """
    
    def on_entry_click(event):
        """
        当输入框被点击时触发的事件处理函数。
        如果当前文本是默认提示文本，则清空输入框并将文本颜色设置为黑色。
        """
        if entry.get() == default_text:
            entry.delete(0, "end")  # 清空输入框中的文本
            entry.config(fg='black')  # 将文本颜色设置为黑色
    
    def on_focusout(event):
        """
        当输入框失去焦点时触发的事件处理函数。
        如果输入框为空，则插入默认提示文本并将文本颜色设置为灰色。
        """
        if entry.get() == '':
            entry.insert(0, default_text)  # 插入默认提示文本
            entry.config(fg='grey')  # 将文本颜色设置为灰色
    
    # 设置输入框的初始文本和颜色
    entry.insert(0, default_text)
    entry.config(fg='grey')
    
    # 绑定输入框的获得焦点和失去焦点事件到相应的处理函数
    entry.bind('<FocusIn>', on_entry_click)
    entry.bind('<FocusOut>', on_focusout)
    """
    <FocusIn>：控件获得焦点时触发该事件。例如，当用户点击输入框或使用 Tab 键将焦点移到输入框时。
    <FocusOut>：控件失去焦点时触发该事件。例如，当用户点击其他控件或使用 Tab 键将焦点移出输入框时。
    <Button-1>：鼠标左键点击时触发该事件。
    <Button-2>：鼠标中键点击时触发该事件。
    <Button-3>：鼠标右键点击时触发该事件。
    <KeyPress>：键盘按键按下时触发该事件。
    <KeyRelease>：键盘按键释放时触发该事件。
    <Enter>：鼠标进入控件区域时触发该事件。
    <Leave>：鼠标离开控件区域时触发该事件。
    """

# 生成按钮点击事件处理函数
def generate_keywords():
    global folder_path
    keyword_list = entry_keywords.get().strip().split()  # 获取输入框中的关键词，去除首尾空格并按空格分割

    ## 使用集合可能会改变元素顺序
    # keyword_list = list(set(keyword_list))
    keyword_list = list(dict.fromkeys(keyword_list))

    # current_directory = os.getcwd()
    folder_from_entry = entry_folder.get()
    if folder_from_entry != "请输入视频目录地址..." and folder_from_entry != "":
        folder_path = folder_from_entry
    else:
        Label_tip.config(text="使用默认目录！")

    # 什么都不写
    if not keyword_list:
        Label_tip.config(text="正在使用0.txt！空格分隔关键词, 两个t内放文件名: t文件名t")
        filename = '0' + ".txt"
        # print(text_file)
        text_path = os.path.join(folder_path, filename)
        # if os.path.isfile(text_path):
        with open(text_path, 'r') as file:
            keywords = file.read()
            keywords = keywords.splitlines()
        # print(keywords)
        # 相同的元素只出现一次
        keywords = list(set(keywords))
        key_listbox.delete(0, tk.END)
        for item in keywords:
            key_listbox.insert(tk.END, item)
        return
        
    # 正常情况 ['111', '222', '333', 't123t']
    # 如果写了关键词和文件名，执行下面的代码
    last_keyword = keyword_list[-1]
    if len(keyword_list) > 1 and last_keyword.startswith('t') and last_keyword.endswith('t'):  # 判断最后一个关键词是否用引号包围
        # keyword_list.extend(keyword_list)  # 将关键词添加到列表中
        # 如果 Entry 更新框中已经有文字，则在其后面加上空格再加入关键词
        # if entry_update_Name.get():
        #     entry_update_Name.insert(tk.END, " ")
        # entry_update_Name.insert(tk.END, ' '.join(keywords))  # 将关键词显示在 Entry 更新框中

        # 文本文件的名字
        filename = last_keyword.strip('t') + ".txt"
        keyword_list.pop() # pop移除最后一个元素
        text_path = os.path.join(folder_path, filename)
        # 将原有的文本内容取出,对照,去重
        if os.path.isfile(text_path):
            with open(text_path, 'r') as file:
                keywords = file.read()
                keywords = keywords.splitlines()
            # extend 方法会将第二个列表的所有元素添加到第一个列表的末尾。
            keyword_list.extend(keywords)
            keyword_list = list(set(keyword_list))
        # 创建文本文件，用于存储关键词列表
        with open(text_path, "a") as file:
            file.write('\n'.join(keyword_list))
            file.write('\n')
        Label_tip.config(text="关键词列表已生成，并保存到文件：" + filename)
        # 将关键词放到关键词表中
        key_listbox.delete(0, tk.END)
        for item in keyword_list:
            key_listbox.insert(tk.END, item)
        return
    
    # 第一个为名称的情况//只输入"名称"的情况
    first_keyword = keyword_list[0]
    if first_keyword.startswith('t') and first_keyword.endswith('t'):
        filename = first_keyword.strip('t') + ".txt"
        # print(filename)
        text_path = os.path.join(folder_path, filename)
        # print(text_path)
        if os.path.isfile(text_path):# 检查给定路径是否指向一个文件
            with open(text_path, 'r') as file:
                keywords = file.read()
                keywords = keywords.splitlines()
                # print(keywords)
        keywords = list(set(keywords))
        key_listbox.delete(0, tk.END)
        for item in keywords:
            key_listbox.insert(tk.END, item)
        return

    # 只有关键词的情况
    filename = '0' + ".txt"
    text_path = os.path.join(folder_path, filename)
    # 将原有的文本内容取出,对照,去重
    if os.path.isfile(text_path):
        with open(text_path, 'r') as file:
            keywords = file.read()
            keywords = keywords.splitlines()
        # extend 方法会将第二个列表的所有元素添加到第一个列表的末尾。
        keyword_list.extend(keywords)
        keyword_list = list(set(keyword_list))
    with open(text_path, "a") as file:
        file.write('\n'.join(keyword_list))
        file.write('\n')
    Label_tip.config(text="关键词列表已生成，并保存到文件：" + filename)
    key_listbox.delete(0, tk.END)
    for item in keyword_list:
        key_listbox.insert(tk.END, item)
    return
    
# 双击键词列表项事件处理函数
def on_key_listbox_double_click(event):
    # 获取双击选中的项目索引
    index = key_listbox.curselection()
    if index:
        # 获取选中的项目内
        selected_item = key_listbox.get(index)
        # entry_update_Name.delete(0, tk.END)  # 清空 entry_update_Name 中的内容
        if entry_update_Name.get() == "输入名称":
            entry_update_Name.delete(0, tk.END)
            entry_update_Name.insert(0, "_")
            entry_update_Name.insert(0, selected_item)  # 将选中的项目内容插入 entry_update_Name 框
            return
        entry_update_Name.insert(0, "_")
        entry_update_Name.insert(0, selected_item)  # 将选中的项目内容插入 entry_update_Name 框
        return

# 过滤按钮
def timeFilter():
    filtered_files = [file for file in videofiles_list 
                     if file['time'] is not None and startTime <= file['time'] <= endTime]
    
    # 更新显示列表
    listbox.delete(0, tk.END)
    listbox_box.delete(0, tk.END)
    
    # 按文件名排序
    filtered_files.sort(key=lambda x: os.path.basename(x['path']).lower())
    
    for file in filtered_files:
        duration_str = format_duration(file['time'])
        listbox.insert(tk.END, filter_unicode(os.path.basename(file['path']) + duration_str))
        listbox_box.insert(tk.END, filter_unicode(file['path']))
    
    entry_tip_updata(f"过滤到 {len(filtered_files)} 个视频")




# 在 `UI.py` 文件中添加新的按钮和函数
def button_jingpin1():
    move_video("精品")

def button_yiban1():
    move_video("一般")

def button_buxing1():
    move_video("不行")

def button_haixing1():
    move_video("还行")

def move_video(folder_name):
    # 获取当前视频文件的目录
    video_path = entry_box.get()
    if video_path == "":
        entry_tip_updata("请先选择视频文件！")
        return

    # 获取当前选中的索引
    index = listbox.curselection()
    if not index:  # 如果没有选中项
        entry_tip_updata("请先选择视频文件！")
        return

    # 获取选中的项目内容
    video_path = listbox_box.get(index[0])  # box里的全部是有目录的

    # 检查文件是否存在
    if not os.path.exists(video_path):
        entry_tip_updata("视频文件不存在！请刷新列表或重新搜索")
        # 从列表中移除不存在的文件
        listbox.delete(index)
        listbox_box.delete(index)
        # 清空 entry_box 和 entry
        entry_box.delete(0, tk.END)
        entry.delete(0, tk.END)
        entry.insert(0, "当前选中的视频")
        return

    # 获取当前视频件的文件名
    video_name = os.path.basename(video_path)
    
    # 获取视频文件的上一级目录
    parent_directory = os.path.dirname(os.path.dirname(video_path))
    
    # 检查目标文件夹是否存在，如果不存在则创建
    target_folder = os.path.join(parent_directory, folder_name)
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    
    # 检查视频文件是否已经存在于目标文件夹中
    new_video_path = os.path.join(target_folder, video_name)
    if os.path.exists(new_video_path):
        # 弹出提示框，询问用户是否要移动视频文件
        result = messagebox.askyesno("提示", f"视频已存在于 {folder_name} 文件夹中，是否要覆盖？")
        if result:
            # 移动视频文件到目标文件夹
            os.replace(video_path, new_video_path)
            entry_tip_updata("移动成功：" + new_video_path)
        else:
            entry_tip_updata("视频未移动")
            return
    else:
        # 移动视频文件到目标文件夹
        os.rename(video_path, new_video_path)
        entry_tip_updata("移动成功：" + new_video_path)

    # 移动文件后更新全局视频列表
    global video_list, videofiles_list
    video_list = [path for path in video_list if path != video_path]
    videofiles_list = [item for item in videofiles_list if item['path'] != video_path]

    # 从显示列表中移除已移动的文件
    listbox.delete(index)
    listbox_box.delete(index)
    
    # 清空 entry_box 和 entry
    entry_box.delete(0, tk.END)
    entry.delete(0, tk.END)
    entry.insert(0, "当前选中的视频")

# 在主函数之前添加文件夹过滤函数
def folder_filter():
    selected_folder = folder_combobox.get()
    if not selected_folder:
        entry_tip_updata("请先选择文件夹！")
        return
        
    if not videofiles_list:
        entry_tip_updata("请先刷新列表！")
        return

    # 获取当前目录
    folder_from_entry = entry_folder.get()
    if folder_from_entry != "请输入视频目录地址..." and folder_from_entry != "":
        current_folder = folder_from_entry
    else:
        current_folder = folder_path
    
    # 过滤出目标文件夹中的视频
    filtered_paths = []
    for file in videofiles_list:
        # 获取视频文件所在的文件夹路径
        video_folder = os.path.dirname(file['path'])
        # 如果文件夹名称匹配，则添加到过滤列表中
        if os.path.basename(video_folder) == selected_folder:
            filtered_paths.append(file['path'])

    # 更新显示列表
    listbox.delete(0, tk.END)
    listbox_box.delete(0, tk.END)
    
    if not filtered_paths:
        entry_tip_updata(f"在 {selected_folder} 文件夹中没有找到��频！")
        return
        
    # 按文件名排序
    filtered_paths.sort(key=lambda x: os.path.basename(x).lower())
    
    for item in filtered_paths:
        listbox.insert(tk.END, filter_unicode(os.path.basename(item)))
        listbox_box.insert(tk.END, filter_unicode(item))
    
    entry_tip_updata(f"在 {selected_folder} 文件夹中找到 {len(filtered_paths)} 个视频")

"""
grid布局
row=row_number：指定小部件放置在第几行。
column=column_number：指定小部件放置在第几列。
rowspan=row_span：指定小部件占据多少行，默认为 1。
columnspan=column_span：指定小部件占多少列，默认为 1。
"""
def setup_shortcuts():
    root.bind('<Control-p>', lambda e: button_play_video1())  # Ctrl+P 播放
    root.bind('<Control-n>', lambda e: button_play_next1())   # Ctrl+N 下一个
    root.bind('<Control-q>', lambda e: button_close_video1()) # Ctrl+Q 闭
    root.bind('<Control-r>', lambda e: button_update_list1()) # Ctrl+R 刷新列表

def create_context_menu():
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="播放", command=button_play_video1)
    context_menu.add_command(label="下一个", command=button_play_next1)
    context_menu.add_separator()
    context_menu.add_command(label="移动到精品", command=button_jingpin1)
    context_menu.add_command(label="移动到还行", command=button_haixing1)
    context_menu.add_command(label="移动到一般", command=button_yiban1)
    context_menu.add_command(label="移动到不行", command=button_buxing1)
    return context_menu

def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)

def safe_execute(func, error_message="操作失败"):
    try:
        return func()
    except Exception as e:
        entry_tip_updata(f"{error_message}: {str(e)}")
        return None

def save_config():
    config = {
        'last_folder': entry_folder.get(),
        'window_size': f"{root.winfo_width()}x{root.winfo_height()}",
        'potplayer_path': POTPLAYER_PATH
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return {}

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("简单界面")
    # 设置窗口初大小为 500x700 像素
    root.geometry("1150x820")

    # 提示框
    Label_tip = tk.Label(root, width=120, justify="center")
    Label_tip.config(text = '提示消息: 请先输入视频目录！')
    # entry_tip.config(state = "readonly")
    Label_tip.pack()



    # 输入地址框
    entry_folder = tk.Entry(root, width=30, fg='grey')
    entry_folder.insert(0, '请输入视频目录地址...')
    entry_folder.bind('<FocusIn>', on_entry_click)
    entry_folder.bind('<FocusOut>', on_focus_out)
    entry_folder.pack()
    # 输入框
    entry = tk.Entry(root, width=60, justify = "center")
    set_default_text(entry, "当前选中的视频")
    entry.pack()



    # 创建一个Frame容器来放置按钮
    button_frame = tk.Frame(root)
    button_frame.pack()
    # 播放按钮
    button_play_video = tk.Button(button_frame, text="播放", command=button_play_video1)
    button_play_video.pack(side="left", padx=1)
    # 播放下一个按钮
    button_play_next = tk.Button(button_frame, text="播放下一个", command=button_play_next1)
    button_play_next.pack(side="left", padx=1)
    # 关闭按钮 
    button_close_video = tk.Button(button_frame, text="关闭", command=button_close_video1)
    button_close_video.pack(side="left", padx=1)



  # 创建一个Frame容器来放置改名框与按钮
    changeName_frame = tk.Frame(root)
    changeName_frame.pack()
    # 改名框
    entry_update_Name = tk.Entry(changeName_frame,width=50, justify="center")
    set_default_text(entry_update_Name, "输入名称")
    entry_update_Name.pack(side="left")
    # 改名按钮
    button_update_Name = tk.Button(changeName_frame, text="改名", command=button_update_Name1)
    button_update_Name.pack(side="left", padx=1) 

    # 用于存储双击的视频的完整路径，用于子文件的情况
    entry_box = tk.Entry()
    # 用于存储列表里的完整的路径名
    listbox_box = tk.Listbox()


  # 创建一个Frame容器来放置搜索框
    search_frame = tk.Frame(root)
    search_frame.pack()
    # 搜索框
    entry_search = tk.Entry(search_frame, width=30, justify="center")
    set_default_text(entry_search, "搜索框(关键词按空格分割)")
    entry_search.pack(side="left")
    # 搜索按钮
    button_search = tk.Button(search_frame, text="搜索", command=search_videos)
    button_search.pack(side="left", padx=1)



   # 创建一个Frame容器来放置过滤框
    filter_frame = tk.Frame(root)
    filter_frame.pack()
    # 创建标签
    label = tk.Label(filter_frame, text="请选择一个选项:")
    label.pack(side="left", pady=10)
    # 定义下拉框选项
    options = ["10s以下", "10s~30s", "30s~1分钟", "1分钟~5分钟", "5分钟~10分钟", 
              "10分钟~30分钟", "30分钟~1小时", "1小时以上", "精品", "还行", "一般", "不行", "不限"]
    
    # 创建Combobox
    combobox = ttk.Combobox(filter_frame, values=options)
    combobox.pack(side="left", pady=10)
    combobox.set("不限")  # 设置默认值
    # 处理选择事件
    def on_select(event):
        # print("你选择了:", combobox.get())
        selectText = combobox.get()
        global startTime
        global endTime
        if selectText == "10s以下":
            startTime = 0
            endTime = 10
        elif selectText == "10s~30s":
            startTime = 10
            endTime = 30
        elif selectText == "30s~1分钟":
            startTime = 30
            endTime = 60
        elif selectText == "1分钟~5分钟":
            startTime = 60
            endTime = 300
        elif selectText == "5分钟~10分钟":
            startTime = 300
            endTime = 600
        elif selectText == "10分钟~30分钟":
            startTime = 600
            endTime = 1800
        elif selectText == "30分钟~1小时":
            startTime = 1800
            endTime = 3600
        elif selectText == "1小时以上":
            startTime = 3600
            endTime = 99999999999
        elif selectText == "不限":
            startTime = 0
            endTime = 99999999999
    # 过滤按钮
    timeFilter_button = tk.Button(filter_frame, text="过滤测试", command=timeFilter)
    timeFilter_button.pack(side="left", pady=5)
    combobox.bind("<<ComboboxSelected>>", on_select)

    # 更新列表按钮
    button_update_list = tk.Button(filter_frame, text="刷新视频列表", command=lambda: button_update_list1())
    button_update_list.pack(side="left")
    # 创建 Listbox 组件（展示视频 的列表）
    listbox = tk.Listbox(root, width=150)
    listbox.pack()
    # 绑定双击列表项事件
    """
    <Double-Button-1>：表示鼠标左键双击事件。
    <Double-Button-2>：表示鼠标中键双击事件。
    <Double-Button-3>：表示鼠标右键双击事件。
    """
    listbox.bind("<Double-Button-1>", on_listbox_double_click)


    
    # 创建 关键词 Listbox 组件
    key_listbox = tk.Listbox(root, width=20)
    key_listbox.bind('<Double-Button-1>', on_key_listbox_double_click)
    key_listbox.pack()




    # 输入框
    entry_keywords = tk.Entry(root, justify="center")
    entry_keywords.pack(pady=5)
    # 生成按钮
    button_generate = tk.Button(root, text="关键字(文件)生成", command=generate_keywords)
    button_generate.pack(pady=5)



    # 在 `UI.py` 文件中添加新的按钮
    button_jingpin = tk.Button(button_frame, text="精品", command=button_jingpin1)
    button_jingpin.pack(side="left", padx=1)

    button_haixing = tk.Button(button_frame, text="还行", command=button_haixing1)
    button_haixing.pack(side="left", padx=1)

    button_yiban = tk.Button(button_frame, text="一般", command=button_yiban1)
    button_yiban.pack(side="left", padx=1)

    button_buxing = tk.Button(button_frame, text="不行", command=button_buxing1)
    button_buxing.pack(side="left", padx=1)

    # 在 filter_frame 中添加新的控件
    # 创建标签
    folder_label = tk.Label(filter_frame, text="选择文件夹:")
    folder_label.pack(side="left", pady=10, padx=5)
    
    # 创建文件夹下拉框
    folder_options = ["精品", "还行", "一般", "不行"]
    folder_combobox = ttk.Combobox(filter_frame, values=folder_options, width=10)
    folder_combobox.pack(side="left", pady=10)
    folder_combobox.set("精品")  # 设置默认值
    
    # 创建文件夹过滤按钮
    folder_filter_button = tk.Button(filter_frame, text="文件夹过滤", command=folder_filter)
    folder_filter_button.pack(side="left", pady=5, padx=5)

    setup_shortcuts()

    context_menu = create_context_menu()
    listbox.bind("<Button-3>", show_context_menu)  # 绑定右键点击事件

    # setup_drag_drop()  # 暂时注释掉这行，等安装了 tkinterdnd2 包后再启用

    config = load_config()
    if config.get('last_folder'):
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, config['last_folder'])
    root.protocol("WM_DELETE_WINDOW", lambda: (save_config(), root.destroy()))

    # 启动事件循环
    root.mainloop()

