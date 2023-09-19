import os
import shutil

class FileHelper:
    def __init__(self, path):
        # 初始化文件路径
        # 检查路径是否存在
        if not os.path.exists(path):
            raise Exception("文件路径不存在")
        self.path = path

    # 获取文件列表基础函数
    def get_file_list(self,recursive:bool=True,full_path:bool=False):
        """
        获取文件列表
        :param recursive: 是否递归
        :param full_path: 是否返回完整路径
        :return: 文件列表
        """
        file_list = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_list.append(file if not full_path else os.path.join(root, file))
            if not recursive:
                break
        return file_list
    
    # 获取文件夹列表基础函数
    def get_dir_list(self,recursive:bool=True,full_path:bool=False):
        """
        获取文件夹列表
        :param recursive: 是否递归
        :param full_path: 是否返回完整路径
        :return: 文件夹列表
        """ 
        dir_list = []
        for root, dirs, files in os.walk(self.path):
            for dir in dirs:
                dir_list.append(dir if not full_path else os.path.join(root, dir))
            if not recursive:
                break
        return dir_list
    
    # 仅仅获取当前目录下的所有文件
    def get_file_list_in_dir(self,full_path:bool=False):
        # return os.listdir(self.path)
        """
        获取当前目录下的所有文件
        :param full_path: 是否返回完整路径
        :return: 所有文件列表
        """
        return self.get_file_list(recursive=False,full_path=full_path)

    # 获取当前目录下的所有文件夹
    def get_dir_list_in_dir(self,full_path:bool=False):
        """
        获取当前目录下的所有文件夹
        :param full_path: 是否返回完整路径
        :return: 所有文件夹列表
        """
        return self.get_dir_list(recursive=False,full_path=full_path)

    # 获取当前目录下的所有文件以及文件夹
    def get_file_dir_list_in_dir(self,full_path=False):
        """
        获取当前目录下的所有文件以及文件夹 (非递归)
        :param full_path: 是否返回完整路径
        :return: 所有文件以及文件夹列表
        """
        return self.get_file_list(recursive=False,full_path=full_path)+ self.get_dir_list(recursive=False,full_path=full_path)

    # 获取当前文件夹内所有文件以及 nested 文件
    def get_file_in_dir_recursive(self,full_path=False):
        """
        获取当前文件夹内所有文件以及 nested 文件 (递归)
        :param full_path: 是否返回完整路径
        :return: 所有文件以及 nested 文件列表
        """
        all_files = self.get_file_list(recursive=True,full_path=True)
        return all_files if full_path else [x.replace(self.path,'').strip(os.sep) for x in all_files]
    
    # 复制文件列表到目标位置
    @staticmethod
    def copy_files_to(files: list, target_dir: str, overwrite=False):
        """
        复制文件列表到目标位置
        :param files: 文件列表
        :param target_dir: 目标文件夹
        :param overwrite: 是否覆盖
        :return: 复制成功列表，覆写成功列表
        """
        copied_files = []
        overwrited_files = []
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for file in files:
            src_file = os.path.abspath(file)
            dst_file = os.path.join(target_dir, os.path.basename(src_file))
            if not os.path.exists(dst_file):
                shutil.copy2(src_file, dst_file)
                copied_files.append(src_file)
            elif overwrite:
                shutil.copy2(src_file, dst_file)
                overwrited_files.append(src_file)
                
        return copied_files,overwrited_files

    # 获取文件名字 (带拓展名)
    @staticmethod
    def get_file_name(file_path):
        """
        获取文件名字 (带拓展名)
        :param file_path: 文件路径
        :return: 文件名 (带拓展名)
        """
        if os.path.isfile(file_path):
            return os.path.basename(file_path)
    
    # 获取文件名字 (不带拓展名)
    @staticmethod
    def get_file_name_without_extension(file_path):
        """
        获取文件名字 (不带拓展名)
        :param file_path: 文件路径
        :return: 文件名 (不带拓展名)
        """
        if os.path.isfile(file_path):
            return os.path.splitext(FileHelper.get_file_name(file_path))[0] # type: ignore
    
    # 获取文件拓展名
    @staticmethod
    def get_file_extension(file_path):
        """
        获取文件拓展名
        :param file_path: 文件路径
        :return: 文件拓展名
        """
        if os.path.isfile(file_path):
            return os.path.splitext(FileHelper.get_file_name(file_path))[1] # type: ignore

    # 获取文件大小
    @staticmethod
    def get_file_size(file_path):
        """
        获取文件大小
        :param file_path: 文件路径
        :return: 文件大小
        """
        if os.path.isfile(file_path):
            return os.path.getsize(file_path)