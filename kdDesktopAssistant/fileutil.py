# coding: utf-8
import os
from shutil import copy2
cur_dir = os.path.dirname(os.path.realpath(__file__))
def get_file_realpath(file):
    return os.path.join(cur_dir,file)
def check_and_create(absolute_file_path):
    slash_last_index = absolute_file_path.rindex("/")
    path = absolute_file_path[:slash_last_index]
    # 检查目录
    if os.path.exists(path) is not True:
        os.makedirs(path)
    elif os.path.isdir(path) is not True:
        print(path, "is no a dir,delete and create a dir")
        os.remove(path)
        os.makedirs(path)
    # 检查文件
    if not os.path.exists(absolute_file_path):
        copy2(get_file_realpath("data/profile.ini"), absolute_file_path)

def check_and_create_dir(absolute_dir_path):
    if os.path.exists(absolute_dir_path) is not True:
        os.makedirs(absolute_dir_path)
    elif os.path.isdir(absolute_dir_path) is not True:
        print(absolute_dir_path, "is no a dir,delete and create a dir")
        os.remove(absolute_dir_path)
        os.makedirs(absolute_dir_path)
