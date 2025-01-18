import os
import sys
import dotenv

import gzip
import json

import pandas as pd
import numpy as np

dotenv.load_dotenv('.env')    
PATH_DATA = os.environ.get('PATH_OPENSKY') + os.environ.get('PATH_REL_DATA')

def get_news_feed() -> pd.DataFrame:
    PATH_FEED_POSTS = PATH_DATA + 'feed_posts/'
    date_parser = lambda x: pd.to_datetime(x, format='%Y%m%d%H%M')
    data = []

    # Open the gzipped JSONL file
    with gzip.open(PATH_FEED_POSTS + 'News.jsonl.gz', 'rt') as f:
        for line in f:
            data.append(json.loads(line))

    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Assuming the date column is named 'date_column'
    df['date'] = df['date'].apply(date_parser)
    return df

def get_posts_from_nos(user_id: int) -> pd.DataFrame:
    df_news_feed = get_news_feed()
    return df_news_feed[df_news_feed.user_id == user_id]
    
