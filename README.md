# opensky

THE DATA

Data from ~4 million users, representing ~81% of all registered accounts, includes 235 million posts with metadata such as timestamps, language, likes, and replies.
The data was collected from Bluesky using its official Developer API. Sentiment analysis was conducted with RoBERTa, a model based on Google’s BERT architecture.
The News feed is a highly popular custom feed containing posts from verified news outlets. Custom feeds are a feature of Bluesky that allows users to create personalized feeds, which can be bookmarked and accessed at any time.
Disclaimer regarding sentiment scores: Our analysis uses only the sentiment label and does not take into account the confidence score associated with each label.

https://docs.bsky.app/docs/starter-templates/custom-feeds  
https://huggingface.co/docs/transformers/en/model_doc/roberta  
https://arxiv.org/abs/2404.18984  
