# Clean-Twitter
Scrub tweets and likes from your Twitter account.

## Requirements
- Python 3.6
- [tweepy](https://github.com/tweepy/tweepy)

## Usage

1. Save the script into whatever directory you wish
2. In that same directory create a config.ini file and copy the following, filling in your details where appropriate
```
[AUTH]
api_key=
api_secret_key=
access_token=
access_token_secret=
```
3. Open your command prompt and navigate to your directory
4. Running ```python cleantwitter.py --tweets``` will delete all of your tweets. Similarly, ```python cleantwitter.py --likes``` will delete all of your likes.
   
   You can use both flags in tandem and it will delete both. Adding the ```--log``` flag will save tweet information to a .txt file in your directory before deleting.
