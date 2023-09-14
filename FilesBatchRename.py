import os
import sys
import shutil
from FileHelper import FileHelper
from SearchTextInFileHelper import SearchTextInFileHelper

files_folder_path_global = 'C:\\Users\\ZHANGYUN\\Desktop\\StandaloneFolder.txt'
Keys_2_search_path_Global = 'C:\\Users\\ZHANGYUN\\Desktop\\Keys.txt'


def read_path_from_txt(path):
    # 读取文件内容
    with open(path, 'r') as f:
        line = f.readline()
        return line
    
def read_keys_from_txt(path):
    lines=[]
    # 读取文件内容
    with open(path, 'r') as f:
        lines = f.readlines()
        return [x.strip('\n') for x in lines]

# 在文件夹内所有文件中查询是否存在字符串 queryStr, 
# 如果文件中存在 , 则返回文件名
def find_strs_in_file(queryStrs, rootDir):
    # 遍历文件夹，获取文件名列表
    fileNameList = FileHelper(rootDir).get_file_list_in_dir(full_path=True)
    #  多线程遍历文件名列表，在文件中查询字符串
    for index,fileName in enumerate(fileNameList):
        print("  {0}.Seaching in {1}:".format(index,fileName.split('\\')[-1]))
        with open(fileName, 'r', encoding='utf-8') as f:
            content = f.read()
            for number,queryStr in enumerate(queryStrs):
                if queryStr in content:
                    print("    >>> {0}.|| {1} || have been found in || {2} ||".format(number,queryStr,fileName.split('\\')[-1]))





if __name__ == "__main__":
    # rootDir= "D:\\TempFIles\\StandaLoneLicense V14Cp1"
    # rootDir= "\\\\HQAZRNDFS01.corp.aspentech.com\\data\\Quarterly Licensing Testing for Aspen Releases\\Licensing Testing - August and V14.2 Nov 2023\\UAT UPL1 - V14.2 Nov\\Product Team License Files\\Standalone"
    
    rootDir = read_path_from_txt(files_folder_path_global)
    queryStrings = read_keys_from_txt(path=Keys_2_search_path_Global)
    files_list = FileHelper(rootDir).get_file_list_in_dir(full_path=True)
    result = []
    for file in files_list:
        result = SearchTextInFileHelper(file).search_text_in_file_exact(queryStrings[0])
        print(result)



    # print("-"*32)
    # for index,queryStr in enumerate(queryStrings):
    #     print("- {0}. {1}".format(index,queryStr))
    # print("-"*32)



    # find_strs_in_file(queryStrings, rootDir)



    # #获取目标路径下的所有文件，并且输出到 文本 ALlFiles.txt 里
    # # 获取目标路径
    # rootDir = "C:\\Users\\ZHANGYUN\\Desktop\\PlanGeneration"
    # fHelper = FileHelper(rootDir)
    # # 获取所有文件
    # fileList = fHelper.get_file_in_dir_recursive()
    # # 获取所有文件名
    # fileNameList = [name for name in fileList]
    # # 根据文件 extension 排序
    # fileNameList.sort(key=lambda x: x.split(".")[-1])
    # # 输出
    # with open("AllFiles.txt", "w") as f:
    #     for name in fileNameList:
    #         f.write(name + "\n")
    # # 复制一份 AllFiles.txt，并且重命名为 RenameThem.txt
    # shutil.copy2("AllFiles.txt", "RenameThem.txt")