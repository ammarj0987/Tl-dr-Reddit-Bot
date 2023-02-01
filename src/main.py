import time
import praw
import os
import openai
import keys
from transformers import pipeline

# If a post is bigger than postLength limit, summarize it.
postLength = 2500
# list of subreddits that the bot will run on.
subreddits = ["AmItheAsshole", "relationship_advice"]

# checks if the post is not a pinned post and does not have tldr already
def validPost(post):
    if len(post.selftext) < postLength or post.stickied == True:
        return False
    lowered = post.selftext.lower()
    if "tldr" in lowered or "tl:dr" in lowered:
        return False
    return True

# text: text in the post waiting to be summarized
# model: openAI or huggingface
# returns a summarized response from model
def getResponse(text, model):
    if model == "openAI":
        return openAI(text)
    elif model == "huggingface":
        return huggingface(text)

# get summary from opneAI
def openAI(text):
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

# get summary from inference API
def huggingface(text):
    summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")
    return summarizer(text)

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

def connectReddit():
    # conenct to reddit
    reddit = praw.Reddit(
        client_id=keys.CLIENT_ID,
        client_secret=keys.CLIENT_SECRET,
        user_agent=keys.USER_AGENT,
        username =keys.USERNAME,
        password =keys.PASSWORD
    )

    # connect to subreddits
    for i in subreddits:
        for post in reddit.subreddit(i).hot(limit=10):
            if (validPost(post)):
                res = getResponse(post.selftext, "hugggingface")
                comment = processText(res)
                #post.reply(comment)
                print(comment)

            #sleep for 11 minutes after commenting
            #time.sleep(660)