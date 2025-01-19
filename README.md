# opensky

THE DATA

Data from ~4 million users, representing ~81% of all registered accounts. 
235 million posts, covering various metadata like timestamps, language, likes, and replies.

The data was scrapped from Bluesky by the official developer API. The sentiment analysis was conducted with roBERTa, based on Googles BERT data model. 

The news feed, is a custom feed with high popularity containing posts from verified news outlets. Custom feeds is a feature of Bluesy to create customised feeds that can be bookmarked and accessed by any time. 

Disclaimer regarding sentiment score: In our analysis we are using only the sentiment label, however we don’t take into account the confidence score of the label.

https://docs.bsky.app/docs/starter-templates/custom-feeds  
https://huggingface.co/docs/transformers/en/model_doc/roberta  
https://arxiv.org/abs/2404.18984  
