from ast import Tuple
import os
import asyncio
import tkinter as tk
from tkinter import Tk, filedialog
from tkinter import messagebox
from FileHelper import FileHelper

user_select_path = ""
temp_notepad_path = os.path.join(os.path.dirname(__file__), "renameTEMP","temp_file_rename_yg.txt")

file_list = []
dir_list = []
file_list_renamed = []
dir_list_renamed = []


def select_directory():
    directory = filedialog.askdirectory()
    dir_fullpath_entry.delete(0, tk.END)
    dir_fullpath_entry.insert(0, directory)
    user_select_path = directory

async def load_files():
    global file_list
    global dir_list
    file_list = []
    dir_list = []
    directory = dir_fullpath_entry.get()
    if directory:
        filehelper = FileHelper(directory)
        file_list = filehelper.get_file_list_in_dir()
        dir_list = filehelper.get_dir_list_in_dir()
    # 根据文件 extension 排序
    file_list.sort(key=lambda x: x.split(".")[-1])
    # 根据文件夹名字排序
    dir_list.sort()
    # 清空 file_dir_listbox
    file_dir_listbox.delete(0, tk.END)
    # 重新添加文件
    for file in file_list:
        file_dir_listbox.insert(tk.END, file)
    file_dir_listbox.insert(tk.END, "~"*20)
    for dir in dir_list:
        file_dir_listbox.insert(tk.END, dir)

async def read_notepad():
    global file_list_renamed
    global dir_list_renamed
    global temp_notepad_path
    file_list_renamed = []
    dir_list_renamed = []
    start_dir = False
    with open(temp_notepad_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("~") and line.endswith("~"):
                start_dir = True
                continue
            if start_dir:
                dir_list_renamed.append(line)
            else:
                file_list_renamed.append(line)
            # 把重新命名后的字符数组加入到 renamed_listbox 里
            file_dir_renamed_listbox.insert(tk.END, line)

async def rename_file_dir():
    global user_select_path
    global file_list
    global dir_list
    global file_list_renamed
    global dir_list_renamed
    if (len(file_list) != len(file_list_renamed)) or (len(dir_list)!= len(dir_list_renamed)):
        # raise ValueError("renamed file or dir is not equal to the original file or dir")
        messagebox.showerror("Error", "renamed file or dir is not equal to the original file or dir")
        return
    # rename files one by one
    for i in range(len(file_list)):
        old_full_path=os.path.join(user_select_path,file_list[i])
        new_full_path=os.path.join(user_select_path,file_list_renamed[i])
        os.rename(old_full_path,new_full_path)
    # rename dirs one by one
    for i in range(len(dir_list)):
        old_full_path=os.path.join(user_select_path,dir_list[i])
        new_full_path=os.path.join(user_select_path,dir_list_renamed[i])
        os.rename(old_full_path,new_full_path)





def set_grid_config(root:Tk,row_column:tuple,row_column_weight:tuple):
    """
    Set the grid config of root

    such as:\n
    row_count,column_count=(4,5)

    row_weight,column_weight = ([1,2,3,4],[1,2,3,4,5])
    """
    row_count,column_count= row_column
    row_weights,column_weights= row_column_weight
    for i in range(row_count):
        root.grid_rowconfigure(i, weight=row_weights[i])
    for i in range(column_count):
        root.grid_columnconfigure(i, weight=column_weights[i])
    return root



app_root = tk.Tk()
app_root.title("Directory Reader")
app_root = set_grid_config(app_root,(3,5),([1,1,1],[1,2,2,1,1]))


# create views
frame_root = tk.Frame(app_root)
dir_fullpath_entry = tk.Entry(frame_root, width=50)
dir_picker_button = tk.Button(frame_root, text="Select Directory", command=select_directory)
load_button = tk.Button(frame_root, text="Modify name by NotePad", command=load_files)
diff_button = tk.Button(frame_root, text="Diff after saving notepad", command=read_notepad)
rename_button = tk.Button(frame_root, text="Rename", command=rename_file_dir)
scrollbar = tk.Scrollbar(app_root)
file_dir_listbox = tk.Listbox(app_root, width=50, height=10)
file_dir_renamed_listbox = tk.Listbox(app_root, width=50, height=10)

# initialize views
frame_root.grid(row=0, column=0, padx=10, pady=10,sticky='we')
dir_picker_button.grid(row=0, column=0)
dir_fullpath_entry.grid(row=0, column=1,columnspan=2)
load_button.grid(row=0, column=3) 
rename_button.grid(row=0, column=4) 
# 一个用于 file_dir_listbox 的 scrollbar
scrollbar.grid(row=1, column=3, sticky='ns')
scrollbar.config(command=file_dir_listbox.yview)
# 一个用于展示当前目录内容的 listbox
file_dir_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
file_dir_renamed_listbox.grid(row=1, column=3, columnspan=2, padx=10, pady=10)
file_dir_listbox.config(yscrollcommand=scrollbar.set)
file_dir_renamed_listbox.config(yscrollcommand=scrollbar.set)
file_dir_listbox.bind('<<ListboxSelect>>', lambda e: print(file_dir_listbox.curselection()))
file_dir_renamed_listbox.bind('<<ListboxSelect>>', lambda e: print(file_dir_listbox.curselection()))


# Start the GUI
app_root.mainloop()
