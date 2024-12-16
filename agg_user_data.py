import os, sys
import dotenv

import pandas as pd
import numpy as np
from tqdm import tqdm

dotenv.load_dotenv('.env')    
PATH_DATA = os.environ.get('PATH_OPENSKY') + os.environ.get('PATH_REL_DATA')
PATH_USER_POSTS = PATH_DATA + 'user_posts/'

def get_df_posts(user_id: int) -> pd.DataFrame:
    global ERROR
    try:
        with open(PATH_USER_POSTS + str(user_id) + '.jsonl') as f:
            return pd.read_json(f, lines=True)
    except Exception as e:
        ERROR = True
        print(f"Exception in get_df_posts: {e}")
        return pd.DataFrame()

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

user_posts_files = os.listdir(PATH_USER_POSTS)
user_ids = [int(f.split('.')[0]) for f in user_posts_files]

df = pd.DataFrame(index=user_ids)

try:
    for user_id, row in tqdm(df.iterrows(), total=len(df)):
        ERROR = False
        df_user_posts = get_df_posts(user_id)

        if df_user_posts.empty:
            ERROR = True

            df.loc[user_id, "instance"] = None
            df.loc[user_id, "langs"] = None
            df.loc[user_id, "min_date"] = None
            df.loc[user_id, "max_date"] = None
            df.loc[user_id, "mean_sent_score"] = None
            df.loc[user_id, "mean_like_count"] = None
            df.loc[user_id, "mean_reply_count"] = None
            df.loc[user_id, "mean_repost_count"] = None
            df.loc[user_id, "n_posts"] = None
            df.loc[user_id, "caught_exception"] = ERROR
            continue

        df.loc[user_id, "instance"] = df_user_posts.loc[0, "instance"] if not df_user_posts.empty else None
        df.loc[user_id, "langs"] = get_langs(df_user_posts)  # Convert list to comma-separated string
        df.loc[user_id, "min_date"], df.loc[user_id, "max_date"] = get_minmax_dates(df_user_posts)
        df.loc[user_id, "mean_sent_score"] = get_mean_sent_score(df_user_posts)
        df.loc[user_id, "mean_like_count"] = get_mean_like_count(df_user_posts)
        df.loc[user_id, "mean_reply_count"] = get_mean_reply_count(df_user_posts)
        df.loc[user_id, "mean_repost_count"] = get_mean_repost_count(df_user_posts)
        df.loc[user_id, "n_posts"] = len(df_user_posts)
        df.loc[user_id, "caught_exception"] = ERROR  

except KeyboardInterrupt:
    print("KeyboardInterrupt")
    print("Saving current progress to 'results/agg_user_data.csv'")
    df.to_csv('results/agg_user_data.csv')

print("Finished")
print("Saving to 'results/agg_user_data.csv'")
df.to_csv('results/agg_user_data.csv')