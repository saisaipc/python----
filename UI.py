# 本项目使用的是 PotPlayer 播放器
import tkinter as tk
import getFileList 
import playVideo
import os
# TODO 关键词查询时的数量可以变一变

# 全局变量，用于存储当前视频列表
# 在函数中用globle表示使用的是全局变量，函数中不能使用同名的变量
video_list = []
folder_path = r"D:\大三下\python视频整理"

video_player = "wmplayer.exe"
video_player = "PotPlayerMini64.exe"

# 双击列表项事件处理函数
def on_listbox_double_click(event):
    # 获取双击选中的项目索引
    index = listbox.curselection()
    if index:
        # 获取选中的项目内容
        selected_item = listbox.get(index)
        selected_item_box = listbox_box.get(index)
        entry_box.delete(0, tk.END)  # 清空 entry_box 中的内容
        entry_box.insert(0, selected_item_box)  # 插入选中的项目内容
        # 将选中的项目显示在 Entry 中
        entry.delete(0, tk.END)  # 清空 Entry 中的内容
        entry.insert(0, selected_item)  # 插入选中的项目内容

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
        entry_box.insert(0, selected_item_box)  # 插入选中的项目内容
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
    user_input = entry.get()
    folder_from_entry = entry_folder.get()
    if user_input == '' or user_input == "当前选中的视频":
        entry_tip_updata("请先双击列表中的视频！")
        return
    if user_input != '' and folder_from_entry != "请输入视频目录地址..." and folder_from_entry != "":
        video_path = entry_box.get()
        playVideo.play_video(video_path)
    else:
        playVideo.play_video(user_input)

# 关闭视频
def button_close_video1():
    global video_player
    pid = None
    old_pid = playVideo.close_video_player(video_player , pid)
    # 返回的是提示时为str，返回的是pid时为int
    if len(str(old_pid)) > 10 :
        entry_tip_updata(f"没有查询到{video_player}")
        return
    msg2 = playVideo.close_video_player(video_player , old_pid)
    entry_tip_updata(msg2)

# 改名按钮
def button_update_Name1():
    # 检测是否选择了视频文件
    oldname = entry.get()
    if oldname != "":
        newname = entry_update_Name.get()
        if newname != "" and newname != "输入名称":
            tip = playVideo.rename_file(oldname, newname)
            entry_tip_updata(tip)
        else:
            entry_tip_updata("请输入名称！")
        return
    entry_tip_updata("请先输入改名文件的名称！")
    return

# 提示框
def entry_tip_updata(msg):
    Label_tip.config(text = msg)

# 更新 Listbox 中添加项目
def button_update_list1():
    global video_list
    global folder_path
    listbox.delete(0, tk.END)
    folder_from_entry = entry_folder.get()
    if folder_from_entry != "请输入视频目录地址..." and folder_from_entry != "":
        # E:\ALL of Games\The Last of Us Part I v1.1.0\学习补丁+修改器+完美全解锁存档+赠品\学习补丁
        folder_path = folder_from_entry
        video_list = getFileList.get_files_list(folder_from_entry)
        entry_tip_updata(f"共查询到 {len(video_list)} 个视频")
    else:
        video_list = getFileList.get_files_list(folder_path)
        entry_tip_updata(f"正使用默认目录，查询到 {len(video_list)} 个视频")
    # 默认按照文件名进行排序
    video_list.sort()
    for item in video_list:
        listbox.insert(tk.END, os.path.basename(item))
        listbox_box.insert(tk.END, item)

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
    # print("这是搜索按钮")
    # test = listbox.get(0)
    # print(test)
    if listbox.get(0) == "":
        entry_tip_updata("请先刷新列表！")
    global video_list
    keywords = entry_search.get().strip().split()  # 获取搜索关键词，去除首尾空格并按空格分割
    if not keywords or entry_search.get() == "搜索框(关键词按空格分割)":
        entry_tip_updata("请先输入文字！")
        return
    # 计算每个视频文件名中包含的关键词数量
    video_score = {}
    for video_path in video_list:
        video_name = os.path.basename(video_path)
        # 对每一个视频进行关键词查找
        score = sum(keyword.lower() in video_name.lower() for keyword in keywords)
        video_score[video_path] = score
    values_list = list(video_score.values())
    if max(values_list) == 0:
        entry_tip_updata("没有查询到对应的视频！")
        return
    else:
        count_non_zero = sum(1 for element in values_list if element != 0)
        entry_tip_updata(f"查询完成! 共有 {count_non_zero} 个视频")
    # 根据得分对视频列表进行排序
    video_list.sort(key=lambda x: -video_score.get(x, 0))
    ## 使用 filter 函数筛选出 sore 字典中值不等于 0 的元素
    after_search_video_list = list(filter(lambda x : video_score.get(x,0) != 0, video_list))
    # 更新列表框中的内容
    listbox.delete(0, tk.END)
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
        # E:\ALL of Games\The Last of Us Part I v1.1.0\学习补丁+修改器+完美全解锁存档+赠品\学习补丁
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
        # 将关键词放到关键词列表中
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
    
# 双击关键词列表项事件处理函数
def on_key_listbox_double_click(event):
    # 获取双击选中的项目索引
    index = key_listbox.curselection()
    if index:
        # 获取选中的项目内容
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

"""
grid布局
row=row_number：指定小部件放置在第几行。
column=column_number：指定小部件放置在第几列。
rowspan=row_span：指定小部件占据多少行，默认为 1。
columnspan=column_span：指定小部件占据多少列，默认为 1。
"""
if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("简单界面")
    # 设置窗口初始大小为 500x700 像素
    root.geometry("500x720")

    # 提示框
    Label_tip = tk.Label(root, width=60, justify="center")
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
    entry = tk.Entry(root, justify = "center")
    set_default_text(entry, "当前选中的视频")
    entry.pack()

    # 播放按钮
    button_play_video = tk.Button(root, text="播放", command=button_play_video1)
    button_play_video.pack()

    # 播放下一个按钮
    button_play_next = tk.Button(root, text="播放下一个", command=button_play_next1)
    button_play_next.pack()

    # 关闭按钮 
    button_close_video = tk.Button(root, text="关闭", command=button_close_video1)
    button_close_video.pack() 

    # 改名框
    #  textvariable="输入名称",
    entry_update_Name = tk.Entry(root, justify="center")
    set_default_text(entry_update_Name, "输入名称")
    entry_update_Name.pack()

    # 改名按钮
    button_update_Name = tk.Button(root, text="改名", command=button_update_Name1)
    button_update_Name.pack() 

    # 用于存储双击的视频的完整路径，用于子文件的情况
    entry_box = tk.Entry()
    # 用于存储列表里的完整的路径名
    listbox_box = tk.Listbox()

    # 搜索框
    entry_search = tk.Entry(root, width=30, justify="center")
    set_default_text(entry_search, "搜索框(关键词按空格分割)")
    entry_search.pack()

    # 搜索按钮
    button_search = tk.Button(root, text="搜索", command=search_videos)
    button_search.pack()

    # 创建 Listbox 组件（展示视频 的列表）
    listbox = tk.Listbox(root, width=150)
    listbox.pack()
    

    # 更新列表按钮
    button_update_list = tk.Button(root, text="刷新视频列表", command=lambda: button_update_list1())
    button_update_list.pack()

    # 绑定双击列表项事件
    """
    <Double-Button-1>：表示鼠标左键双击事件。
    <Double-Button-2>：表示鼠标中键双击事件。
    <Double-Button-3>：表示鼠标右键双击事件。
    """
    listbox.bind("<Double-Button-1>", on_listbox_double_click)

    
    # 创建 关键词 Listbox 组件
    key_listbox = tk.Listbox(root, width=50)
    key_listbox.bind('<Double-Button-1>', on_key_listbox_double_click)
    key_listbox.pack()

    # 输入框
    entry_keywords = tk.Entry(root, justify="center")
    entry_keywords.pack(pady=5)
        # 生成按钮
    button_generate = tk.Button(root, text="关键字(文件)生成", command=generate_keywords)
    button_generate.pack(pady=5)

    # 启动事件循环
    root.mainloop()
