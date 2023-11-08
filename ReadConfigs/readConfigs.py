import os
from configparser import ConfigParser

dir_path = os.path.dirname(os.path.realpath(__file__))
ConfigFile = dir_path+'/../conf/Configurtions.ini'
os_type = os.name   # "nt" - Windows , "posix" - Linux 
if os_type == "nt":
    ConfigFile = dir_path+'\..\conf\Configurtions.ini'



def readConfigFromFile ():
    config = ConfigParser()
    config.read(ConfigFile)
    return config