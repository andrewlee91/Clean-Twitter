import configparser
import sys
import time

import tweepy

config = configparser.ConfigParser()


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


def Rate_Limit(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print(
                "You are currently being rate limited. Waiting for 5 minutes then trying to resume."
            )
            time.sleep(5 * 60)


def Check_Arguments(api):
    if len(sys.argv) == 1:
        print(
            "No argument passed. Run 'python cleantwitter.py tweets' or 'python cleantwitter.py likes'."
        )
        quit()
    else:
        if sys.argv[1].lower() == "tweets":
            Delete_Tweets(api)
        elif sys.argv[1].lower() == "likes":
            Delete_Likes(api)
        else:
            print("Invalid arguement.")
            quit()


def Delete_Tweets(api):
    user_tweets = Rate_Limit(tweepy.Cursor(api.user_timeline).items())

    for tweet in user_tweets:
        print(
            f"Deleting status with id: {tweet.id_str} from user: {tweet.user.screen_name}"
        )
        api.destroy_status(tweet.id_str)


def Delete_Likes(api):
    likes = Rate_Limit(tweepy.Cursor(api.favorites).items())

    for tweet in likes:
        print(
            f"Deleting status with id: {tweet.id_str} from user: {tweet.user.screen_name}"
        )
        api.destroy_favorite(tweet.id_str)


if __name__ == "__main__":
    api = Twitter_Auth()
    Check_Arguments(api)
