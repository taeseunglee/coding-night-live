import os
import sys


# Check OS
platform = sys.platform
if platform == 'win32' or platform == 'win64':
    print('Error: Cannot run in Windows..')
    exit(0)

cmd = 'python3'

# Check Python Version (3 or 2)
if sys.version_info[0] == 2:
    print('Error: Cannot run in Python 2.x..')
    exit(0)

# Install python packages
try:
    import pip
except ImportError:
    print("Installing pip...")
    if platform == 'linux':
        os.system('sudo apt-get install python3-pip')
with open('requirements.txt', 'r') as packages:
    for package in packages:
        if package[0] == '#':
            break
        pip.main(['install', package])

# DB Migration
os.system('%s manage.py migrate' % cmd)

# Admin user setting
os.system('%s manage.py createsuperuserauto' % cmd)

# Install redis-server / nginx
if platform == 'linux':
    os.system('sudo apt-get install redis-server')
    os.system('sudo apt-get install nginx')

# Find nginx location
# nginx = subprocess.checkoutput('sudo find / -name nginx.conf', shell=True)

# Server Deploy
BASE_DIR = os.getcwd()
os.system('sudo rm -rf /etc/nginx/sites-enabled/local_nginx.conf')
os.system('sudo ln -s %s/nginx/local_nginx.conf /etc/nginx/sites-enabled/' % BASE_DIR)

# OAuth setting
os.system('%s manage.py collectstatic' % cmd)
os.system('%s manage.py autodeploy' % cmd)

# Server run
os.system('redis-server &')
os.system('%s manage.py runworker &' % cmd)
os.system('daphne -b 0.0.0.0 -p 8001 coding_night_live.asgi:channel_layer &')
os.system('sudo service nginx start')
