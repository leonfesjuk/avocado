import sys
import os

VIRTUAL_ENV_PATH = '/home/leonfesjuk/venv'

import site
# Цей шлях має відповідати версії Python, яку ви обрали (Python 3.9)
site.addsitedir(f'{VIRTUAL_ENV_PATH}/lib/python3.9/site-packages')

project_home = '/home/leonfesjuk/avocado'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

from asgi_tools.wsgi import WSGIMiddleware
from backend_python.main import app as application_asgi

application = WSGIMiddleware(application_asgi)