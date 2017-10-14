import praw
import re

reddit = praw.Reddit('tldrbot')
subreddit = reddit.subreddit("noveltranslations")
def parse_text(text):
	matchObj = re.search(r'\[Chapter [0-9]+ *\]\(.+\)', text)

	if(matchObj):
		print("------------------ REGEX FOUND ------------------")
		print("Group", matchObj.group())
		## (http:\/\/[a-zA-Z]+\.[a-zA-Z0-9\/\-\.]+)      ((http|https):\/\/[a-zA-Z]+\.[^\)]+)
		link = re.search(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', matchObj.group())
		print("Link:", link.group())
	else:
		print("------------------ REGEX NOT FOUND ------------------")

for submission in subreddit.hot(limit=10):
	print("Title: ", submission.title)
	print("Text: ", submission.selftext)
	parse_text(submission.selftext)

