import praw
import yaml
from urllib.parse import quote_plus

with open('config.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print(e)


def main():
    reddit = praw.Reddit(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        password=config['password'],
        user_agent=config['user_agent'],
        username=config['username']
    )

    subreddit = reddit.subreddit('antiwork')
    for submission in subreddit.stream.submissions():
        process_submission(submission)


def process_submission(submission):
    new_submission_reply_template = 'Top-level comment reply!'
    if len(submission.title.split()) > 10:
        return

    normalized_title = submission.title.lower()
    if 'nestle' in normalized_title:
        url_title = quote_plus(submission.title)
        reply_text = new_submission_reply_template.format(url_title)
        submission.reply(body=reply_text)


if __name__ == 'main':
    main()
