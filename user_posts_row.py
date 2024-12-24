import os, sys
import dotenv

dotenv.load_dotenv('.env')    
PATH_DATA = os.environ.get('PATH_OPENSKY') + os.environ.get('PATH_REL_DATA')
PATH_USER_POSTS = PATH_DATA + 'user_posts/'

import gzip

lines = []
i = 0
with gzip.open(PATH_DATA + 'interactions.csv', 'r') as f:
    while True:
        line = f.readline()       
        i += 1
        print(i, end=' ')