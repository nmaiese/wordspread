from twython import Twython
import os
import json

APP_KEY = 'GQxyGH2hVkqbVGDrGdTQfiIgs'
APP_SECRET = 'kUJK1FqwrKHlQh4twwp2Cjsk5DoLfbZJRbeGVxxprJZ1nqe3bf'
OAUTH_TOKEN = '1300285536-cP7JcbJJD9taOHXP31EkcH9hIWU6alwWD2pgCIr'
OAUTH_TOKEN_SECRET = 'Kn3MuonBsnMLs0hOFSHeK7vVl2yLPIaQqaO0dzATf1mJO'

OUT_FOLDER ='data/'
if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def download_user_timeline(username, out_folder='data/'):
    user_tweets = []
    results = twitter.cursor(twitter.get_user_timeline, screen_name=username, trim_user=0, tweet_mode='extended')
    for tweet in results:
        user_tweets.append(tweet)
        # print('\r%s tweets for %s ' % (len(user_tweets), username), end='')
    with open(out_folder+username+'.json', 'w') as f:
        json.dump(user_tweets,  f, indent=4)
    return user_tweets

