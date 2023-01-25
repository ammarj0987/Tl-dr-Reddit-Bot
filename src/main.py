import time
import praw
import os
import openai
import keys

# If a post is bigger than postLength limit, summarize it.
postLength = 2500

# text: text in the post waiting to be summarized
# returns a summarized response from openAI
def getResponse(text):
    # Load your API key from an environment variable or secret management service
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

# connect to subreddit
subreddit = reddit.subreddit("AmItheAsshole")
for post in subreddit.hot(limit=10):
    if (len(post.selftext) > postLength):
        # print(post.title)
        # print(post.selftext)
        # print(len(post.selftext))
        print("---------------------------")
        res = getResponse(post.selftext)
        comment = processText(res)
        print(comment)

    # sleep for 11 minutes after commenting
    #time.sleep(660)