from flask import Flask, render_template, request, flash, jsonify, session, redirect, Markup
import tweepy

app = Flask(__name__)
app.config.from_object(__name__)

auth = tweepy.OAuthHandler("API_KEY", "API_ACCESS_KEY")
auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")

api = tweepy.API(auth)
exists = False

usernames = ["@FoxNews", "@CNNnewsroom", "@NBCNews"]

def init():
	pass

def cleanTweet(text):
	stopwords = ('http','rt','@', '#')
	textwords = text.split()

	resultwords  = [word for word in textwords if not word.lower().startswith(stopwords)]
	result = ' '.join(resultwords)
	return result

def getTweets(usernames):
	users = []
	for user in usernames:
		user_obj = {
			"name": user,
			"tweets": []
		}
		count = 0
		for tweet in tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items():
			text = unicode(tweet.full_text.encode("utf8"), "utf8")
			text = cleanTweet(text)
			exists = True
			user_obj["tweets"].append(text)
			count += 1
			if count > 10:
				break
			
		if (not exists):
			print("No results were found")
		users.append(user_obj)
	
	exists = False
	return users

@app.route("/")
def home():
	users = getTweets(usernames)
	return render_template("home.html", users=users)

 
if __name__ == "__main__":
	init()
	app.run()