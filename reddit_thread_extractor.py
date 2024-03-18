import praw

# Function to get Reddit thread and original post
def get_reddit_thread(url):
    reddit = praw.Reddit(client_id='c_c9EKVGpkKM7FNqXX2yAQ',
                         client_secret='iDe77_eqt-2tT6daD5U7ebe3QO3kGg',
                         user_agent='reddit_bot')
    submission = reddit.submission(url=url)
    return submission.title, submission.selftext, submission.comments.list()
