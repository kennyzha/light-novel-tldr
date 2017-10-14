import praw
import re

reddit = praw.Reddit('tldrbot')
subreddit = reddit.subreddit("noveltranslations")

def parse_text(text):
	pass

for submission in subreddit.hot(limit=10):
	print("Title: ", submission.title)
	print("Text: ", submission.selftext)
	parse_text(submission.selftext)

