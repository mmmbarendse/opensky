import os
import sys
import dotenv
import json

import pandas as pd
import numpy as np

dotenv.load_dotenv('.env')    
PATH_DATA = os.environ.get('PATH_OPENSKY') + os.environ.get('PATH_REL_DATA')
PATH_USER_POSTS = PATH_DATA + 'user_posts/'

def get_df_posts(user_id: int) -> pd.DataFrame:
    global ERROR
    parse_dater = lambda x: pd.to_datetime(x, format='%Y%m%d%H%M')
    data = []

    try:
        with open(PATH_USER_POSTS + str(user_id) + '.jsonl') as f:
            for line in f:
                data.append(json.loads(line))

        df = pd.DataFrame(data)    
        assert not df.empty, "Empty DataFrame"
        df.date = pd.to_datetime(df.date, format='%Y%m%d%H%M')
    except Exception as e:
        ERROR = True
        #print(f"Exception in get_df_posts: {e}")
        return pd.DataFrame()
    
    return df

def get_langs(df_posts: pd.DataFrame) -> list:
    global ERROR
    try:
        if df_posts.langs.dropna().empty:
            return None
        return ",".join(list(set(df_posts.langs.dropna().sum())))
    except Exception as e:
        ERROR = True
        print(f"Exception in get_langs: {e}")
        return None

def get_minmax_dates(df_posts: pd.DataFrame) -> tuple:
    global ERROR
    try:
        return df_posts.date.min(), df_posts.date.max()
    except Exception as e:
        ERROR = True
        print(f"Exception in get_minmax_dates: {e}")
        return None, None

def get_mean_sent_score(df_posts: pd.DataFrame) -> float:
    global ERROR
    try:
        return df_posts.sent_score.mean()
    except Exception as e:
        ERROR = True
        print(f"Exception in get_mean_sent_score: {e}")
        return None

def get_mean_like_count(df_posts: pd.DataFrame) -> float:
    global ERROR
    try:
        return df_posts.like_count.mean()
    except Exception as e:
        ERROR = True
        print(f"Exception in get_mean_like_count: {e}")
        return None

def get_mean_reply_count(df_posts: pd.DataFrame) -> float:
    global ERROR
    try:
        return df_posts.reply_count.mean()
    except Exception as e:
        ERROR = True
        print(f"Exception in get_mean_reply_count: {e}")
        return None

def get_mean_repost_count(df_posts: pd.DataFrame) -> float:
    global ERROR
    try:
        return df_posts.repost_count.mean()
    except Exception as e:
        ERROR = True
        print(f"Exception in get_mean_repost_count: {e}")
        return None

def get_replies_to_users(df_posts : pd.DataFrame, user_ids : list):
    try:
        replied_to = df_posts.thread_root_author.unique()

        if len(replied_to) == 0:
            return [] 
        
        overlap = list(set(replied_to).intersection(user_ids))
        return overlap
    except Exception as e:
        print(f"Exception in get_replies_to_users: {e}")
        return []