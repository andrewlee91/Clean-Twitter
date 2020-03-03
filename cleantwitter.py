import argparse
import configparser
import os
import sys
import time

import tweepy

directory = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()

parser = argparse.ArgumentParser(
    description="Scrub tweets and likes from your Twitter account."
)

parser.add_argument(
    "--tweets", dest="tweets", help="Delete tweets", action="store_true"
)
parser.add_argument("--likes", dest="likes", help="Unlike tweets", action="store_true")
parser.add_argument(
    "--log", dest="logging", help="Log deleted/unliked tweets", action="store_true"
)


def Load_Config():
    config.read("config.ini")

    api_key = config["AUTH"]["api_key"]
    api_secret_key = config["AUTH"]["api_secret_key"]
    access_token = config["AUTH"]["access_token"]
    access_token_secret = config["AUTH"]["access_token_secret"]

    return api_key, api_secret_key, access_token, access_token_secret


def Twitter_Auth():
    api_key, api_secret_key, access_token, access_token_secret = Load_Config()

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def Delete_Tweets(api, log=False):
    deleted_file = f"{directory}/tweets.txt"
    tweets = tweepy.Cursor(api.user_timeline).items()

    for tweet in tweets:
        if hasattr(tweet, "retweeted_status"):
            if log:
                url = tweet.retweeted_status.entities["urls"][0]["expanded_url"]
                log_message = f"{tweet.text} - {url}\n"
                with open(deleted_file, "a") as log_file:
                    log_file.write(log_message)

            api.unretweet(tweet.id)
        else:
            if log:
                log_message = f"{tweet.created_at}: {tweet.text}\n"
                with open(deleted_file, "a") as log_file:
                    log_file.write(log_message)

            api.destroy_status(tweet.id)


def Delete_Likes(api, log=False):
    unliked_file = f"{directory}/likes.txt"
    likes = tweepy.Cursor(api.favorites).items()

    for tweet in likes:
        if log:
            tweet_url = (
                f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}\n"
            )

            with open(unliked_file, "a") as log_file:
                log_file.write(tweet_url)

        api.destroy_favorite(tweet.id)


if __name__ == "__main__":
    api = Twitter_Auth()
    api.wait_on_rate_limit = True
    api.wait_on_rate_limit_notify = True
    args = parser.parse_args()

    if args.tweets:
        if args.logging:
            Delete_Tweets(api, True)
        else:
            Delete_Tweets(api)

    if args.likes:
        if args.logging:
            Delete_Likes(api, True)
        else:
            Delete_Likes(api)
