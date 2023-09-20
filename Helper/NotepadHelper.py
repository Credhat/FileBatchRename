import subprocess
import os
import time
import platform

import psutil


class DataIOHelper:
    @staticmethod
    def create_file_if_not_exists(filepath):
        if not os.path.exists(filepath):
            folder_path = os.path.dirname(filepath)
            os.makedirs(folder_path, exist_ok=True)
            with open(filepath, "w",encoding="utf-8"):
                pass

    @staticmethod
    def write_content(filepath, content):
        with open(filepath, "w",encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def read_content(filepath):
        with open(filepath, "r",encoding="utf-8") as f:
            return f.read()


class NotepadHelper:
    def __init__(self, filepath):
        self.win_version = platform.win32_ver()
        print("Windows 版本：", self.win_version)
        DataIOHelper.create_file_if_not_exists(filepath)
        self.notepad_path = filepath
        self.process = None

    def open(self):
        DataIOHelper.create_file_if_not_exists(self.notepad_path)
        version = self.win_version[0]
        if int(version) <= 10:
            self.process = subprocess.Popen(["notepad.exe", self.notepad_path])
        else:
            self.process = subprocess.Popen(["Notepad.exe", self.notepad_path])

    def read_content(self):
        return DataIOHelper.read_content(self.notepad_path)

    def write_content(self, content):
        DataIOHelper.write_content(self.notepad_path, content)

    def exists(self, filepath, timeout=2):
        start_time = time.time()
        while time.time() - start_time < timeout:
            for proc in psutil.process_iter():
                try:
                    if proc.name() == "notepad.exe" or proc.name() == "Notepad.exe":
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            time.sleep(0.1)
        return False

    def wait_till_closed(self):
        if self.process is None or self.process.poll() is not None:
            return
        stdout, stderr = self.process.communicate()  # 等待记事本进程完成

    def close(self):
        if self.process is None or self.process.poll() is not None:
            return

        self.process.terminate()  # 终止记事本进程

        # 等待记事本进程终止
        while self.process.poll() is None:
            time.sleep(0.1)

        # 查找记事本进程并终止
        for proc in psutil.process_iter():
            try:
                if proc.name() == "notepad.exe" or proc.name() == "Notepad.exe":
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        self.process = None


# notepad_path = r"C:\Users\Administrator\Desktop\PythonRelated\TestFolder\temp_notepad.txt"

# notepad_helper = NotepadHelper(notepad_path)

# # 打开记事本，如果文件不存在则创建
# DataIOHelper.create_file_if_not_exists(notepad_path)
# # 写入内容
# content = "notepad first written"
# DataIOHelper.write_content(notepad_path, content)
# time.sleep(1)
# notepad_helper.open()
# time.sleep(1)
# notepad_helper.wait_till_closed()
# print("notepad closed")
# # notepad_helper.close_notepad()


# # notepad_helper.write_content(content)

# # 保存并关闭记事本
# notepad_helper.close()
win_version,win_version_full,_,_ = platform.win32_ver()
print("Windows 版本：", win_version)