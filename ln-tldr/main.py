import praw
import re
import requests
import json
import os
from urllib import parse
import psycopg2

## Connecting to reddit
reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     password=os.environ['REDDIT_PASSWORD'],
                     user_agent='light novel chapter summarizer',
                     username=os.environ['REDDIT_USERNAME'])

## conn = sqlite3.connect('database.db')
## Connecting to database
parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS posts(
			id text, title text, submission text)''')

subreddit = reddit.subreddit("noveltranslations")
API_KEY = os.environ['API_KEY']

def parse_text(text):
	chapter_regex_pattern = r'\[.*Chapter [0-9]+.*\]\(.*\)'
	chapter_iters = re.finditer(chapter_regex_pattern, text)
	return chapter_iters


def get_url(matchObj):
	url_regex_pattern = r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
	return re.search(url_regex_pattern, matchObj.group())


smmry_url = "http://api.smmry.com/"
def summarize(api_key, sm_length, chapter_url):
		payload = {"SM_API_KEY" : api_key, "SM_LENGTH" : sm_length, "SM_URL" : chapter_url}
		return requests.get(smmry_url, payload)


for submission in subreddit.new(limit=10):
	c.execute("SELECT count(*) FROM posts WHERE id = ?", (submission.id,))
	data = c.fetchone()[0]
	if data == 1:
		print("Post id %s with title %s has been looked at." % (submission.id, submission.title))
		continue

	print("Post id %s with title %s has not been summarized." % (submission.id, submission.title))
	print("Title: ", submission.title)

	chapter_urls = parse_text(submission.selftext)
	submission_post = ''

	if not chapter_urls:
		continue
		
	for chapter_url in chapter_urls:
		submission_post += '[Chapter Preview:](/s "'
		url = get_url(chapter_url)
		print("Link:", url.group())
		summary = summarize(API_KEY, 7, url.group()).json()

		if summary.get("smi_api_error") is None and summary.get("smi_api_content") is not None:
			submission_post += (summary.get("sm_api_content") + '")' + /n/n)
		else:
			print("There was an error summarizing link ", url.group(), "from post", submission.title)
			submission_post = "Error"
	print("Submission_post is ", submission_post)

	post = (submission.id, submission.title, submission_post,)
	c.execute("INSERT INTO posts VALUES (?,?,?)", post)
	conn.commit()
	submission.reply(submission_post)

conn.close()
