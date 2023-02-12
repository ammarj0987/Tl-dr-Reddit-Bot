import time
import praw
import os
import openai
import keys
import requests
import json

"""
This is the main file that connects to reddit and replies to posts sorting by new
"""

# If a post is bigger than postLength limit, summarize it.
POST_LENGTH = 2500

# list of subreddits that the bot will run on.
SUBREDDITS = ["AmItheAsshole", "relationship_advice"]

# choose model
MODEL = "huggingface"

# connect to huggingface model
API_URL = "https://api-inference.huggingface.co/models/philschmid/bart-large-cnn-samsum"
headers = {"Authorization": f"Bearer {keys.API_TOKEN}"}

# connect to openAI model
openai.api_key = keys.API_KEY

# checks if the post is not a pinned post and does not have tldr already
def validPost(post):
    if len(post.selftext) < POST_LENGTH or post.stickied == True:
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
    response = requests.post(API_URL, headers=headers, json=json.dumps(text))
    ret = response.json()
    return ret[0]['summary_text']
        

# text: AI summary
# returns a clean and readable comment
def processReply(reply):
    index = 0
    for i in range (len(reply)):
        if (reply[i].isalpha()):
            index = i
            break
    retText  = reply[index:]
    return retText

def main():
    # conenct to reddit
    reddit = praw.Reddit(
        client_id=keys.CLIENT_ID,
        client_secret=keys.CLIENT_SECRET,
        user_agent=keys.USER_AGENT,
        username =keys.USERNAME,
        password =keys.PASSWORD
    )

    # connect to subreddits
    for i in SUBREDDITS:
        for post in reddit.subreddit(i).new(limit=10):
            if (validPost(post)):
                res = getResponse(post.selftext, MODEL)
                if (MODEL == "openAI"):
                    comment = processReply(res)
                else:
                    comment = res
                #post.reply(comment)
                print(comment)

            # sleep for 11 minutes after commenting
            #time.sleep(660)

if __name__=="__main__":
    main()
