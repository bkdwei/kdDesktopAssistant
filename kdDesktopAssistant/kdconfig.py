import configparser
from os.path import join,expanduser
from .fileutil import check_and_create


# 配置文件所在位置，每个用户的配置不一样，不宜放到程序所在目录，应放在用户主目录
config_file =join(expanduser('~') , ".config/kdDesktopAssistant/profile.ini")
check_and_create(config_file)
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