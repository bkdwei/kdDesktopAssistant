import configparser
from os.path import join,expanduser,exists
from shutil import copy2
from .fileutil import check_and_create_dir
from kdDesktopAssistant.fileutil import get_file_realpath


# 配置文件所在位置，每个用户的配置不一样，不宜放到程序所在目录，应放在用户主目录
config_dir =join(expanduser('~') , ".config/kdDesktopAssistant/")
config_file =join(expanduser('~') , ".config/kdDesktopAssistant/profile.ini")
db_file =join(expanduser('~') , ".config/kdDesktopAssistant/kdDesktopAssistant.db")

# 复制配置文件到个人目录
def check_config_file():
    check_and_create_dir(config_dir)
    if not exists(config_file):
        copy2(get_file_realpath("data/profile.ini"),config_file)
    if not exists(db_file) :
        copy2(get_file_realpath("data/db/kdDesktopAssistant.db"),db_file)
check_config_file()
cf = configparser.ConfigParser()
cf.read(config_file)

def get_option_value(key):
    return cf.get("global", key)
def get_option_boolean(key):
    return cf.getboolean("global", key)
def get_option_int(key):
    return cf.getint("global", key)
def set_home_session(session_name):
    cf.set("global","home_session",session_name)
    cf.write(open(config_file,"w"))
    cf.read(config_file)
def set_web_mode(mode):
    cf.set("global","web_as_application",str(mode))
    cf.write(open(config_file,"w"))
    cf.read(config_file)
def set_item_size(size):
    cf.set("global","item_size",str(size))
    cf.write(open(config_file,"w"))
    cf.read(config_file)