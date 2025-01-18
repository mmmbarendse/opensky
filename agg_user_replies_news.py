import os, sys
import dotenv

import pandas as pd
import numpy as np
from tqdm import tqdm

from user_eval import get_df_posts, get_langs, get_minmax_dates, get_mean_sent_score, get_mean_like_count, get_mean_reply_count, get_mean_repost_count, get_replies_to_users

dotenv.load_dotenv('.env')    
PATH_DATA = os.environ.get('PATH_OPENSKY') + os.environ.get('PATH_REL_DATA')
PATH_USER_POSTS = PATH_DATA + 'user_posts/'

PATH_RESULTS = os.environ.get('PATH_OPENSKY') + 'results/'
PATH_USER_REPLIES_NEWS = PATH_RESULTS + 'agg_user_replies_news_2.csv'

PATH_FEED_POSTS = PATH_DATA + 'feed_posts/'

if __name__ == '__main__':
    user_posts_files = os.listdir(PATH_USER_POSTS)
    user_ids = [int(f.split('.')[0]) for f in user_posts_files]

    df_news_feed = pd.read_json(PATH_FEED_POSTS + 'News.jsonl.gz', lines=True)
    user_ids_news = df_news_feed.user_id.unique()

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
                df.loc[user_id, "replied_to_nos"] = None
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
            df.loc[user_id, "replied_to_nos"] = ','.join(str(idx) for idx in get_replies_to_users(df_user_posts, user_ids_news))
            df.loc[user_id, "caught_exception"] = ERROR  

    except KeyboardInterrupt as e:
        print(f"Stopped because of KeyboardInterrupt: {e}")
        print(f"Saving current progress to '{PATH_USER_REPLIES_NEWS}'")
        df.to_csv(PATH_USER_REPLIES_NEWS)
        sys.exit(1)

    except Exception as e:
        print(f"Exception in main: {e}")
        print(f"Saving current progress to '{PATH_USER_REPLIES_NEWS}'")
        df.to_csv(PATH_USER_REPLIES_NEWS)
        sys.exit(1)

    print("Finished successfully")
    print(f"Saving aggregated data to '{PATH_USER_REPLIES_NEWS}'")
    df.to_csv(PATH_USER_REPLIES_NEWS)
