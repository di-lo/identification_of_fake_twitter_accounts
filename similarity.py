import tweepy
import requests
import os
import json
import dateutil.parser

#consumer_key = "Vqixgr3RIMAJOpiBd01nf2Viz"
#consumer_secret = "jRuakXNaQUtV1WNv8GSPkzAsHXTXC8jcOS7enXKS6oN8WIKRBd"
consumer_key = "3nVuSoBZnx6U4vzUxf5w"
consumer_secret = "Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

cached_hours = {}

def get_user_tweets(screen_name, return_dict_acc):
    print("Getting Tweets from", screen_name)
    alltweets = []
    outtweets = []
    outtweets_time = []
    text_path = "Twitter-Accounts/" + screen_name + "/text"
    media_path = "Twitter-Accounts/" + screen_name + "/media"
    hours_path = "Twitter-Accounts/" + screen_name + "/hours"
    if os.path.isdir("Twitter-Accounts/" + screen_name + "/"):
        if os.path.isfile(text_path) and os.path.isfile(media_path) and os.path.isfile(hours_path):
            text = json.loads(open(text_path, "r").read())
            media = json.loads(open(media_path, "r").read())
            hours = json.loads(open(hours_path, "r").read())
            try:
                profile_picture = api.get_user(screen_name=screen_name).profile_image_url.replace("normal", "bigger")
            except:
                profile_picture = ""

            print('(CACHED) Done User: ', screen_name)
            return_dict_acc[screen_name] = [text, hours, media, profile_picture]
            return
    else:
        os.mkdir("Twitter-Accounts/" + screen_name + "/")

    try:
        new_tweets = api.user_timeline(screen_name = screen_name, count=200, include_rts=False, exclude_replies=False)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        while len(new_tweets) > 0:      
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, include_rts=False, exclude_replies=False)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
        print('Done User: ', screen_name)
        outtweets = [tweet.text for tweet in alltweets]
        outtweets_time = [tweet.created_at for tweet in alltweets]
    except:
        outtweets = ["Dummy_text"]
        outtweets_time = []

    try:
        media = []
        for tweet in alltweets:
            try:
                if "media" in tweet.entities:
                    media.append(tweet.entities["media"])
            except:
                pass

        for tweet in alltweets:
            if "media" in tweet.extended_entities:
                media.append(tweet.extended_entities["media"])
    except Exception as er:
        print(er)

    
    try:
        profile_picture = api.get_user(screen_name=screen_name).profile_image_url.replace("normal", "bigger")
    except:
        profile_picture = ""

    with open(text_path, "w") as f:
        f.write(json.dumps(outtweets))

    with open(media_path, "w") as f:
        f.write(json.dumps(media))

    with open(hours_path, "w") as f:
        hours = output_hours(outtweets_time, screen_name)
        f.write(json.dumps(hours))


    return_dict_acc[screen_name] = [outtweets, hours, media, profile_picture]
    return return_dict_acc[screen_name]
    

def get_daily_time(acc_1, acc_2):
    diff = 1
    if len(acc_1) == 0 or len(acc_2) == 0:
        return 100
    for i in range(24):
        diff += abs(acc_1[i] - acc_2[i])
    return diff

def output_hours(acc, name):
    global cached_hours
    if name in cached_hours:
        return cached_hours[name]
    try:
        hours = [[int(x.hour) for x in acc].count(j) for j in range(24)]
    except:
        try:
            hours = [[int(dateutil.parser.parse(x).hour) for x in acc].count(j) for j in range(24)]
        except:
            hours = []
    cached_hours[name] = hours
    return hours

def compare_media(acc_1, acc_2):
    similarity = 0
    if len(acc_1) == 0 or len(acc_2) == 0:
        return 100
    for i in acc_1:
        max_similarity = 0
        for j in acc_2:
            r = requests.post(
                "https://api.deepai.org/api/image-similarity",
                data={
                    'image1': i[0]["media_url"],
                    'image2': j[0]["media_url"],
                },
                headers={'api-key': '7b7d4109-d598-4103-aac1-e4ab821c39a6'}
            )
            sim = int(r.json()["output"]["distance"])
            sim = 100 - sim
            if sim > max_similarity:
                max_similarity = sim
        similarity += max_similarity
    if similarity <= 0:
        similarity = 1
    similarity = similarity / len(acc_1)
    return similarity