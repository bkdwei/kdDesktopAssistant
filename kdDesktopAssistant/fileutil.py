# coding: utf-8
import os
cur_dir = os.path.dirname(os.path.realpath(__file__))
def get_file_realpath(file):
    return os.path.join(cur_dir,file)

def check_and_create_dir(absolute_dir_path):
    if not os.path.exists(absolute_dir_path) :
        os.makedirs(absolute_dir_path)
    elif not os.path.isdir(absolute_dir_path) :
        print(absolute_dir_path, "is no a dir,delete and create a dir")
        os.remove(absolute_dir_path)
        os.makedirs(absolute_dir_path)
