import os
import sys
import dotenv

import pandas as pd
import numpy as np

dotenv.load_dotenv('.env')    
PATH_DATA = os.environ.get('PATH_OPENSKY') + os.environ.get('PATH_REL_DATA')

def get_news_feed() -> pd.DataFrame:
    PATH_FEED_POSTS = PATH_DATA + 'feed_posts/'
    df_news_feed = pd.read_json(PATH_FEED_POSTS + 'News.jsonl.gz', lines=True)
    return df_news_feed

def get_posts_from_nos(user_id: int) -> pd.DataFrame:
    df_news_feed = get_news_feed()
    return df_news_feed[df_news_feed.user_id == user_id]
    
