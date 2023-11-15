import os
import asyncio
import tkinter as tk
from tkinter import Event, Tk, filedialog
from tkinter import messagebox
from tkinter import font
from Helper.FileHelper import FileHelper
from Helper.NotepadHelper import NotepadHelper


user_select_path = ""
temp_notepad_path = os.path.join(os.path.dirname(__file__), "renameTEMP", "temp_file_rename_yg.txt")

file_list = []
dir_list = []
file_dir_splitter = "-"
file_list_renamed = []
dir_list_renamed = []


# def set_grid_config(root: Tk, row_column: tuple, row_column_weight: tuple):
#     """
#     Set the grid config of root

#     such as:\n
#     row_count,column_count=(4,5)


#     row_weight,column_weight = ([1,2,3,4],[1,2,3,4,5])
#     """
#     row_count, column_count = row_column
#     row_weights, column_weights = row_column_weight
#     for i in range(row_count):
#         root.grid_rowconfigure(i, weight=row_weights[i])
#     for i in range(column_count):
#         root.grid_columnconfigure(i, weight=column_weights[i])
#     return root

class RenameThemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rename Them")
        self.initialize_views()
        self.loop = asyncio.get_event_loop()

    def initialize_views(self):
        self.create_views()
        self.lay_views()
        self.Configure_views()
        self.binding_view()

    def create_views(self):
        # Create views
        # frame
        self.frame_top = tk.Frame(self.root)
        self.frame_bottom = tk.Frame(self.root)
        # entry
        self.dir_fullpath_entry = tk.Entry(self.frame_top, width=50)
        # button
        self.dir_picker_button = tk.Button(self.frame_top, text="1. Select Directory")
        self.modify_button = tk.Button(self.frame_top, text="2. Modify name by NotePad")
        self.diff_button = tk.Button(self.frame_top, text="3. Diff after saving notepad")
        self.rename_button = tk.Button(self.frame_top, text="4. Rename")
        # scrollbar
        self.scrollbar = tk.Scrollbar(self.frame_bottom)
        # listbox
        self.file_dir_listbox = tk.Listbox(self.frame_bottom, width=50, height=10)
        self.file_dir_renamed_listbox = tk.Listbox(self.frame_bottom, width=50, height=10)

    def lay_views(self):
        # Grid layout
        # frame
        self.frame_top.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="we")
        self.frame_bottom.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        # entry
        self.dir_fullpath_entry.grid(row=0, column=1, sticky="we", padx=10)
        # button
        self.dir_picker_button.grid(row=0, column=0, padx=(10, 0))
        self.dir_fullpath_entry.config(width=50)  # Set the minimum width to 200
        self.modify_button.grid(row=0, column=2, padx=(0, 10))
        self.diff_button.grid(row=0, column=3, padx=(0, 10))
        self.rename_button.grid(row=0, column=4, padx=(0, 10))
        # scrollbar
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        # listbox
        self.file_dir_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.file_dir_renamed_listbox.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    def Configure_views(self):
        # Configure resizing behavior
        # frame root
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # frame top
        self.frame_top.grid_columnconfigure(0, weight=0)
        self.frame_top.grid_columnconfigure(1, weight=1)
        self.frame_top.grid_columnconfigure(2, weight=0)
        self.frame_top.grid_columnconfigure(3, weight=0)
        # frame bottom
        self.frame_bottom.grid_rowconfigure(0, weight=1)
        self.frame_bottom.grid_columnconfigure(0, weight=1)
        self.frame_bottom.grid_columnconfigure(1, weight=0)
        self.frame_bottom.grid_columnconfigure(2, weight=1)
        # universal properties
        Font8 = font.Font(size=8)
        Font10 = font.Font(size=10, family="Arial")
        Font12 = font.Font(size=12, family="Consolas")
        Font12Bold = font.Font(size=12, family="Arial", weight="bold")
        Font14 = font.Font(size=14)
        Font14Bold = font.Font(size=14, family="Arial", weight="bold")
        # entry
        self.dir_fullpath_entry.configure(font=Font10, state="readonly")
        # button
        self.diff_button.configure(font=Font10)
        self.modify_button.configure(font=Font10)
        self.dir_picker_button.configure(font=Font10)
        self.rename_button.configure(font=Font12Bold)
        # listbox
        self.file_dir_listbox.configure(font=Font12)
        self.file_dir_renamed_listbox.configure(font=Font12)

    def binding_view(self):
        # command bindings
        # button
        self.dir_picker_button.config(command=self.select_directory)
        self.modify_button.config(command=self.write_open_notepad)
        self.diff_button.config(command=self.read_notepad)
        self.rename_button.config(command=self.rename_file_dir)
        # scrollbar
        self.scrollbar.config(command=self.file_dir_listbox.yview)
        self.scrollbar.config(command=self.file_dir_renamed_listbox.yview)
        # Event bindings
        # listbox
        self.file_dir_listbox.bind("<<ListboxSelect>>", lambda e: self.on_listbox_select(e, self.file_dir_listbox))
        self.file_dir_renamed_listbox.bind("<<ListboxSelect>>", lambda e: self.on_listbox_select(e, self.file_dir_renamed_listbox))

    def on_listbox_select(self, current_event: Event, listbox):
        """
        当列表框中的某一项被选中时触发的回调函数。

        参数:
        - current_event: 当前事件对象。
        - listbox: 被选中的列表框。

        """

        selected_indices = listbox.curselection()
        if current_event.widget is self.file_dir_listbox:
            for i in range(self.file_dir_renamed_listbox.size()):
                self.file_dir_renamed_listbox.itemconfigure(i, background="", fg="black")
            # 如果是文件目录列表框被点击
            print("file_dir_listbox 被点击")
            try:
                for index in selected_indices:
                    print(" >>> No.{0} --- {1} 被点击".format(index, listbox.get(index)))
                    self.file_dir_renamed_listbox.itemconfigure(index, background="sky blue", fg="white")
            except:
                pass
        elif current_event.widget is self.file_dir_renamed_listbox:
            for i in range(self.file_dir_listbox.size()):
                self.file_dir_listbox.itemconfigure(i, background="", fg="black")
            # 如果是重命名后的文件目录列表框被点击
            print("file_dir_renamed_listbox 被点击")
            try:
                for index in selected_indices:
                    print(" >>> No.{0} --- {1} 被点击".format(index, listbox.get(index)))
                    self.file_dir_listbox.itemconfigure(index, background="sky blue", fg="white")
            except:
                pass

    def select_directory(self):
        global user_select_path
        directory = filedialog.askdirectory(initialdir=".")
        if directory != "":
            self.dir_fullpath_entry.configure(state=tk.NORMAL)
            self.dir_fullpath_entry.delete(0, tk.END)
            self.dir_fullpath_entry.insert(0, directory)
            user_select_path = directory
            self.dir_fullpath_entry.configure(state="readonly")
            self.run_async(self.load_file_dir_in_listbox_async())

    def write_open_notepad(self):
        self.run_async(self.write_open_notepad_async())

    def read_notepad(self):
        self.run_async(self.read_notepad_async())

    def rename_file_dir(self):
        self.run_async(self.rename_file_dir_async())

    def run_async(self, coro):
        loop = self.loop
        try:
            loop.run_until_complete(coro)
        except Exception as e:
            print(e)
    

    async def load_file_dir_in_listbox_async(self):
        global file_list
        global dir_list
        file_list = []
        dir_list = []
        directory = self.dir_fullpath_entry.get()
        if directory:
            filehelper = FileHelper(directory)
            file_list = await asyncio.to_thread(filehelper.get_file_list_in_dir)
            dir_list = await asyncio.to_thread(filehelper.get_dir_list_in_dir)
        # 根据文件 extension 排序
        file_list.sort(key=lambda x: x.split(".")[-1])
        # 根据文件夹名字排序
        dir_list.sort()
        # 清空 file_dir_listbox
        self.file_dir_listbox.delete(0, tk.END)
        # 重新添加文件
        for file in file_list:
            self.file_dir_listbox.insert(tk.END, file)
        self.file_dir_listbox.insert(tk.END, file_dir_splitter * 20)
        for dir in dir_list:
            self.file_dir_listbox.insert(tk.END, dir)

    async def write_open_notepad_async(self):
        global temp_notepad_path
        global file_list
        global dir_list
        notepad = NotepadHelper(temp_notepad_path)
        output = ""
        for file in file_list:
            output += file + "\n"
        output += file_dir_splitter * 20 + "\n"
        for dir in dir_list:
            output += dir + "\n"
        notepad.write_content(output)
        notepad.open()
        # notepad.wait_till_closed()
        # notepad.read_content()

    async def read_notepad_async(self):
        global file_list_renamed
        global dir_list_renamed
        global temp_notepad_path
        self.file_dir_renamed_listbox.delete(0, tk.END)
        file_list_renamed = []
        dir_list_renamed = []
        start_dir = False
        with open(temp_notepad_path, "r",encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith(file_dir_splitter) and line.endswith(file_dir_splitter):
                    start_dir = True
                    self.file_dir_renamed_listbox.insert(tk.END, file_dir_splitter * 20)
                    continue
                if start_dir:
                    dir_list_renamed.append(line)
                else:
                    file_list_renamed.append(line)
                # 把重新命名后的字符数组加入到 renamed_listbox 里
                self.file_dir_renamed_listbox.insert(tk.END, line)

    async def rename_file_dir_async(self):
        global user_select_path
        global file_list
        global dir_list
        global file_list_renamed
        global dir_list_renamed
        if (len(file_list) != len(file_list_renamed)) or (len(dir_list) != len(dir_list_renamed)):
            # raise ValueError("renamed file or dir is not equal to the original file or dir")
            messagebox.showerror("Error", "renamed file or dir is not equal to the original file or dir")
            return
        try:
            # rename files one by one
            for i in range(len(file_list)):
                old_full_path = os.path.join(user_select_path, file_list[i])
                new_full_path = os.path.join(user_select_path, file_list_renamed[i])
                if old_full_path != new_full_path:
                    await asyncio.to_thread(os.rename, old_full_path, new_full_path)
            # rename dirs one by one
            for i in range(len(dir_list)):
                old_full_path = os.path.join(user_select_path, dir_list[i])
                new_full_path = os.path.join(user_select_path, dir_list_renamed[i])
                if old_full_path != new_full_path:
                    await asyncio.to_thread(os.rename, old_full_path, new_full_path)
            messagebox.showinfo("Success", "Rename Success.")
        except Exception as e:
            messagebox.showerror("Error", "Rename Failed, no file(s) renamed.\nError message:{0}".format(e))

    def __del__(self):
        self.loop.close()


if __name__ == "__main__":
    app_root = tk.Tk()
    app = RenameThemApp(app_root)
    app_root.mainloop()
