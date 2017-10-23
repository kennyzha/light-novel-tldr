import praw
import re
import requests
import json

reddit = praw.Reddit('tldrbot')
subreddit = reddit.subreddit("noveltranslations")
API_KEY = ""
def parse_text(text):
	chapter_regex_pattern = r'\[Chapter [0-9]+ *\]\(.+\)'
	chapter_iters = re.finditer(chapter_regex_pattern, text)

	for matchObj in chapter_iters:
		url_regex_pattern = r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
		search = re.search(url_regex_pattern, matchObj.group())
		print("Link:", search.group())
##		print_summarys(API_KEY, 40, search.group())
	return chapter_iters


smmry_url = "http://api.smmry.com/"
def print_summarys(api_key, sm_length, chapter_url):
		payload = {"SM_API_KEY" : api_key, "SM_LENGTH" : sm_length, "SM_URL" : chapter_url}
		r = requests.get(smmry_url, payload)
		print(r.text)

for submission in subreddit.new(limit=100):
##	print("Title: ", submission.title)
##	print("Text: ", submission.selftext)
	chapter_urls = parse_text(submission.selftext)
