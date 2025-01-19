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
PATH_USER_POSTS = PATH_DATA + 'user_posts/'

PATH_RESULTS = os.environ.get('PATH_OPENSKY') + 'results/'
PATH_USER_REPLIES_NEWS_POSTS = PATH_RESULTS + 'agg_user_replies_news_posts_2.csv'
PATH_ALL_SENTIMENTS = os.environ.get('PATH_OPENSKY') + 'results/all_sentiments_over_time.csv'

df_news_posts = pd.read_csv(PATH_USER_REPLIES_NEWS_POSTS)
bm_first_depth = (df_news_posts.reply_to == df_news_posts.thread_root)
df_news_posts = df_news_posts[bm_first_depth]
df_news_posts.dropna(subset=['sent_label'], inplace=True)
df_news_posts['date'] = pd.to_datetime(df_news_posts['date'], errors='coerce')

sent_label_mapping = { 0: 'negative', 1: 'neutral', 2: 'positive'}
df_news_posts.loc[:, 'sent_label'] = df_news_posts.sent_label.map(sent_label_mapping)

df_all_replies = pd.read_csv(PATH_ALL_SENTIMENTS, index_col=0)
df_all_replies.loc[:, 'sent_label'] = df_all_replies.sent_label.map(sent_label_mapping)
df_all_replies['date'] = pd.to_datetime(df_all_replies['date'], errors='coerce')

# Removing all posts present in the news feed replies df
bm_not_in_news_feed = ~df_all_replies.post_id.isin(df_news_posts.post_id)
df_all_replies = df_all_replies[bm_not_in_news_feed]

reply_counts = df_all_replies.groupby('reply_to').size().sort_values(ascending=False).reset_index(name='count')

# Calculate the cumulative sum
cumulative_replies = reply_counts['count'].cumsum()
cumulative_replies = cumulative_replies / cumulative_replies.max()
origin = pd.Series([0])
cumulative_replies = pd.concat([origin, cumulative_replies]).reset_index(drop=True)
cumulative_replies.reset_index(drop=True)[1e6]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(cumulative_replies)
ax.set_xlabel('Number of posts')
ax.set_ylabel('Proportion of total replies')
ax.set_title('Proportion of total replies by non-news post')

news_reply_threshold = 100000
ax.vlines(news_reply_threshold, 0, 1, color='red', linestyle='--')

intersection_y = cumulative_replies.iloc[news_reply_threshold] if news_reply_threshold < len(cumulative_replies) else 1
ax.scatter(news_reply_threshold, intersection_y, color='blue')
ax.annotate(f'Prop. news below threshold: {intersection_y:.2f}', 
            xy=(news_reply_threshold, intersection_y), 
            xytext=(news_reply_threshold + 50, intersection_y - 0.1),
            arrowprops=dict(facecolor='black', shrink=1))

ax.grid(True)
fig.show()
fig.savefig(f'{PATH_RESULTS}/figs/prop_total_replies_t{news_reply_threshold}.png')
del fig, ax

relevant_news_posts = reply_counts.head(news_reply_threshold).reply_to.values
df_all_replies = df_all_replies[df_all_replies.reply_to.isin(relevant_news_posts)]
num_sent_replies = df_all_replies.groupby(['reply_to', 'sent_label']).size().unstack()

normalized_df = num_sent_replies.apply(lambda x: x / x.sum(), axis=1)

if 'negative' in normalized_df.columns:
    normalized_df = normalized_df.sort_values(by='negative', ascending=False)

# Plot the normalized bar chart
fig, ax = plt.subplots(figsize=(10, 6))
normalized_df.plot(kind='bar', stacked=True, figsize=(10, 6), width=1, edgecolor='none', ax=ax)
ax.set_xlabel('Individual non-news posts')
ax.set_ylabel('Proportion per sentiment in replies')
ax.set_title('Normalized Sentiment Distribution by Individual Non-News Post')

ax.set_ylim(0,1)

xticks = range(0, len(normalized_df), 10000)
ax.set_xticks(xticks)
ax.set_xticklabels(xticks)

fig.savefig(f'{PATH_RESULTS}/figs/normalized_sentiment_distribution_t{news_reply_threshold}.png')
fig.show()

