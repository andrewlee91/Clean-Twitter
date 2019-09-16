# Clean-Twitter
A small script to scrub tweets and likes from your Twitter account.

## Requirements
- Python 3.6
- [tweepy](https://github.com/tweepy/tweepy)

## Usage

1. Download  the script into whatever directory you wish
2. In that same directory create a config.ini file
3. Open config.ini in notepad and paste the following, filling in your details where appropriate
```
[AUTH]
api_key=
api_secret_key=
access_token=
access_token_secret=
```
4. Open your command prompt and navigate to your directory
5. Run "python cleantwitter.py tweets" to delete all of your tweets or "python cleantwitter.py likes" to delete all of your likes

## To-Do
- [ ] Proper error handling 
- [ ] Improved command line usage
- [ ] Save deleted tweets/likes in an external file
- [ ] Delete tweets before/after a specified date