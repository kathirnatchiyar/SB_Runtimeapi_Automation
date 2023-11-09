import multiprocessing
import os
#from dotenv import load_dotenv
#load_dotenv()

name = "Gunicorn config for FastAPI - TutLinks.com"

accesslog = "/opt/SB_Runtimeapi_Automation_Beta/gunicorn-access.log"
errorlog = "/opt/SB_Runtimeapi_Automation_Beta/gunicorn-error.log"

bind = "10.8.0.2:5000"

worker_class = "Uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count () * 2 + 1
worker_connections = 1024
backlog = 2048
max_requests = 5120
timeout = 120
keepalive = 2

debug = os.environ.get("debug", "false") == "true"
reload = debug
preload_app = False 
daemon = False 
