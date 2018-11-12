#
# src/scraper.py
# 

import os
import django
import time

# Add api to system path to faciliate importing of modules from it
import sys 
sys.path.append('api')

# Django setup to interface with api through django 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.api.settings')
django.setup()

if __name__ == "__main__":
    while True:
        print("running scraper....")
        time.sleep(1)
    
