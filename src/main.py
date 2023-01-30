import time
import praw
import os
import openai
import keys

# If a post is bigger than postLength limit, summarize it.
postLength = 2500
# list of subreddits that the bot will run on.
subreddits = ["AmItheAsshole", "relationship_advice"]

# checks if the post is not a pinned post and does not have tldr already
def validPost(post):
    if len(post.selftext) < postLength or post.stickied == True:
        return False
    lowered = post.selftext.lower()
    words = lowered.split()
    length = len(words)
    for i in reversed[length]:
        if "tldr" in words[i] or "tl;dr" in words[i]:
            return False
    return True

# text: text in the post waiting to be summarized
# returns a summarized response from openAI
def getResponse(text):
    openai.api_key = keys.API_KEY
    myPrompt = text + " Tl;dr"
    response = openai.Completion.create(
        model="text-davinci-003", 
        prompt=myPrompt, 
        temperature=0.7, 
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )
    return response["choices"][0]["text"]

# text: AI summary
# returns a clean and readable comment
def processText(text):
    retText = ""
    index = 0
    for i in range (len(text)):
        if (text[i].isalpha()):
            index = i
            break
    retText  = text[index:]
    return retText

# conenct to reddit
reddit = praw.Reddit(
    client_id=keys.CLIENT_ID,
    client_secret=keys.CLIENT_SECRET,
    user_agent=keys.USER_AGENT,
    username =keys.USERNAME,
    password =keys.PASSWORD
)

# connect to subreddits
for subreddit in subreddits:
    for post in subreddit.hot(limit=10):
        if (validPost()):
            res = getResponse(post.selftext)
            comment = processText(res)
            post.reply(comment)

        #sleep for 11 minutes after commenting
        time.sleep(660)