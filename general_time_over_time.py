import os, sys
import dotenv

import pandas as pd
import numpy as np
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt

sys.path.append(os.environ.get('PATH_OPENSKY'))
from user_eval import get_df_posts 
from news_outlet_eval import get_news_feed, get_posts_from_nos

dotenv.load_dotenv('.env')    
PATH_DATA = os.environ.get('PATH_OPENSKY') + os.environ.get('PATH_REL_DATA')
PATH_ALL_SENTIMENTS = os.environ.get('PATH_OPENSKY') + 'results/all_sentiments_over_time.csv'

df = pd.read_csv(PATH_ALL_SENTIMENTS)

df.groupby('sent_label').agg({'sent_label': 'count', 'sent_score': 'mean'})
sent_label_mapping = { 0: 'negative', 1: 'neutral', 2: 'positive'}
df.loc[:, 'sent_label'] = df.sent_label.map(sent_label_mapping)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df[df['date'].notna()]
df.set_index('date', inplace=True)

resample_frequency = '3D'  # Change this to 'T' for minutes, 'S' for seconds, etc.
df_resampled = df.groupby('sent_label').resample(resample_frequency).size().unstack(fill_value=0)
df_sent_labels = df_resampled.T#.reset_index().set_
df_sent_labels.loc[:, 'total'] = df_sent_labels.sum(axis=1)

print(f"Total number of posts: {df_sent_labels.total.sum()}, Maximum number of posts in a week: {df_sent_labels.total.max()}")

df_sent_labels.loc[:, 'negative'] = df_sent_labels.negative / df_sent_labels.total    
df_sent_labels.loc[:, 'neutral'] = df_sent_labels.neutral / df_sent_labels.total
df_sent_labels.loc[:, 'positive'] = df_sent_labels.positive / df_sent_labels.total
df_sent_labels.drop(columns=['total'], inplace=True)

df_sent_labels.to_csv(os.environ.get('PATH_OPENSKY') + 'results/resampled_sentiments_over_time_3d.csv')

