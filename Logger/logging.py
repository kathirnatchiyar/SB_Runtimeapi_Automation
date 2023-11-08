import os
import logging
from ReadConfigs.readConfigs import readConfigFromFile

config = readConfigFromFile()


log_file = config.get('Logging', 'log_file')
log_level = config.get('Logging', 'log_level')
dir_path = os.path.dirname(os.path.realpath(__file__))

log_dir = "{}/../logs".format(dir_path)
log_file_path = "{}/{}".format(log_dir, log_file)

os_type = os.name   # "nt" - Windows , "posix" - Linux 
if os_type == "nt":
    log_dir = "{}\..\logs".format(dir_path)
    log_file_path = "{}\{}".format(log_dir, log_file)
    
print("Configuration file path: ", log_file_path)
# Check if the directory exists
if not os.path.exists(log_dir):
    # If it doesn't exist, create it
    os.makedirs(log_dir)

if log_level == "DEBUG":
    logLevel = logging.DEBUG
elif log_level == "INFO":
    logLevel = logging.INFO
elif log_level == "WARN":
    logLevel = logging.WARN
elif log_level == "ERROR":
    logLevel = logging.ERROR
    
logging.basicConfig(
    filename=log_file_path,
    level=logLevel,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
)

def logger(cname):
    logger = logging.getLogger(cname)
    return logger