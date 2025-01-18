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
PATH_USER_ALL_SENTIMENTS_OVER_TIME = PATH_RESULTS + 'all_sentiments_over_time.csv'

if __name__ == '__main__':
    user_posts_files = os.listdir(PATH_USER_POSTS)

    try:
        df_list = []

        for file in tqdm(user_posts_files):
            df_posts = get_df_posts(str(file.split('.')[0]))

            if df_posts.empty:
                continue

            bm_first_depth = (df_posts.reply_to == df_posts.thread_root)
            df_posts = df_posts[bm_first_depth]

            if df_posts.empty:
                continue

            df_posts = df_posts.loc[~df_posts.sent_score.isna(), ['post_id', 'user_id', 'date', 'labels', 'sent_label', 'sent_score', 'reply_to', 'thread_root']]

            if df_posts.empty:
                continue

            df_list.append(df_posts)

    except KeyboardInterrupt as e:
        print(f"Stopped because of KeyboardInterrupt: {e}")
        print(f"Saving current progress to '{PATH_USER_ALL_SENTIMENTS_OVER_TIME}'")
        df = pd.concat(df_list)
        df.to_csv(PATH_USER_ALL_SENTIMENTS_OVER_TIME)
        sys.exit(1)

    except Exception as e:
        print(f"Exception in main: {e}")
        print(f"Saving current progress to '{PATH_USER_ALL_SENTIMENTS_OVER_TIME}'")
        df = pd.concat(df_list)
        df.to_csv(PATH_USER_ALL_SENTIMENTS_OVER_TIME)
        sys.exit(1)

    print("Finished successfully")
    print(f"Saving aggregated data to '{PATH_USER_ALL_SENTIMENTS_OVER_TIME}'")
    df = pd.concat(df_list)
    df.to_csv(PATH_USER_ALL_SENTIMENTS_OVER_TIME)
