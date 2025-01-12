import os, sys
import dotenv

import pandas as pd
import numpy as np
from tqdm import tqdm

from user_eval import get_df_posts 

dotenv.load_dotenv('.env')    
PATH_DATA = os.environ.get('PATH_OPENSKY') + os.environ.get('PATH_REL_DATA')
PATH_USER_POSTS = PATH_DATA + 'user_posts/'

PATH_RESULTS = os.environ.get('PATH_OPENSKY') + 'results/'
PATH_USER_REPLIES_NEWS = PATH_RESULTS + 'agg_user_replies_news.csv'
PATH_USER_REPLIES_NEWS_POSTS = PATH_RESULTS + 'agg_user_replies_news_posts.csv'

PATH_FEED_POSTS = PATH_DATA + 'feed_posts/'

if __name__ == '__main__':
    user_posts_files = os.listdir(PATH_USER_POSTS)
    user_ids = [int(f.split('.')[0]) for f in user_posts_files]

    df_news_feed = pd.read_json(PATH_FEED_POSTS + 'News.jsonl.gz', lines=True)
    user_ids_news = df_news_feed.user_id.unique()
    
    df_agg_user_replies_news = pd.read_csv(PATH_USER_REPLIES_NEWS, index_col=0)
    rel_user_ids = list(df_agg_user_replies_news.dropna(subset='replied_to_nos').index)

    df_replies_list = []

    try:
        for user_id in tqdm(rel_user_ids):
            df_user_posts = get_df_posts(user_id)

            if df_user_posts.empty:
                continue
            
            df_replies_to_nos = df_user_posts[df_user_posts.thread_root_author.isin(user_ids_news)]

            if df_replies_to_nos.empty:
                continue

            df_replies_list.append(df_replies_to_nos)
            
    except KeyboardInterrupt as e:
        print(f"Stopped because of KeyboardInterrupt: {e}")
        print(f"Saving current progress to '{PATH_USER_REPLIES_NEWS_POSTS}'")
        pd.concat(df_replies_list).to_csv(PATH_USER_REPLIES_NEWS_POSTS, index=False)
        sys.exit(1)

    except Exception as e:
        print(f"Exception in main: {e}")
        print(f"Saving current progress to '{PATH_USER_REPLIES_NEWS_POSTS}'")
        pd.concat(df_replies_list).to_csv(PATH_USER_REPLIES_NEWS_POSTS, index=False)
        sys.exit(1)

    print("Finished successfully")
    print(f"Saving aggregated data to '{PATH_USER_REPLIES_NEWS_POSTS}'")
    pd.concat(df_replies_list).to_csv(PATH_USER_REPLIES_NEWS_POSTS, index=False)
