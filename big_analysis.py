import tweepy
import requests
import os
import json
import dateutil.parser
from similarity import *
from tf import *
import sys

def search_for_accounts(text, screen_name):
    users = api.search_users(screen_name)
    tweets = api.search_tweets(text)
    accounts = set()
    for i in users:
        accounts.add(i.screen_name)
    for i in tweets:
        accounts.add(i.user.screen_name)
    try:
        accounts.remove(screen_name)
    except:
        pass
    return list(accounts)

def big_analysis(screen_name):
    return_dict_acc = {}
    similar_accounts = set()
    acc = get_user_tweets(screen_name, return_dict_acc)
    visited = []
    for i in return_dict_acc[screen_name][0]:
        [similar_accounts.add(i) for i in search_for_accounts(i, screen_name)]
        print("Got some accounts")
        for similar_account in similar_accounts:
            if similar_account not in visited and similar_account != screen_name:
                visited.append(similar_account)

                related_accounts = {}
                tweets = {}
                jobs = []

                accs = [screen_name, similar_account]
                accs_pictures = {}
                filter_quality = .2

                output_accs = []

                get_user_tweets(similar_account, return_dict_acc)

                
                for proc in jobs:
                    proc.join()

                for i in accs:
                    try:
                        if len(return_dict_acc[i][3]) > 1:
                            accs_pictures[i] = return_dict_acc[i][3]
                        else:
                            accs_pictures[i] = "https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png"
                    except:
                        accs_pictures[i] = "https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png"
                for i in accs:
                    tweets[i] = ' '.join(return_dict_acc[i][0])

                print("-"*30)

                if len(tweets.keys()) < 2:
                    print("Not enough ACCs")
                    exit()

                ref, data = tf(tweets)
                visited = []
                for ind, ary in enumerate(ref):
                    for i, el in enumerate(ary):
                        if i != ind:
                            if str(ind) + "_" + str(i) in visited:
                                continue
                            visited.append(str(i) + "_" + str(ind))
                            tfidf = el
                            try:
                                acc_1 = return_dict_acc[accs[ind]]
                                acc_2 = return_dict_acc[accs[i]]
                            except:
                                print(return_dict_acc[accs[i]], return_dict_acc[accs[ind]])

                            hours1 = acc_1[1]
                            hours2 = acc_2[1]

                            time_similarity = 5 * ( 1 / get_daily_time(hours1, hours2) )
                            media_similarity = 5 * ( 1 / compare_media(acc_1[2], acc_2[2]))
                            el += time_similarity
                            el += media_similarity
                            el = min(el, 100)

                            similar = False

                            if el >= filter_quality:
                                related_accounts[ind] = None
                                related_accounts[i] = None
                                similar = True
                                print(ind, i)

                            sim_accs_list = list(similar_accounts)
                            for j in range(len(sim_accs_list)):
                                if sim_accs_list[j] == accs[i]:
                                    set_i = j
                            similarity_percentage_round = round(int(el*100)/10)*10
                            output_accs.append({"id": "0_" + str(set_i+1), "name": accs[ind] + " & " + accs[i], "hours1": hours1, "hours2": hours2, "tfidf": min(99, tfidf*100)+1, "media": min(99, media_similarity*100)+1, "hours_sim": min(99, time_similarity*100)+1, "acc1_profile": accs[ind], "acc2_profile": accs[i], "similarity": similar, "similarity_percentage": int(el*100), "similarity_percentage_round": int(similarity_percentage_round)})
                accounts = []
                x = 0
                for acc in tweets:
                    if x in related_accounts:
                        accounts.append(acc)
                    x += 1

                out_path = "Twitter-Accounts/Big_Analysis_" + screen_name + "/" + similar_account + "/"
                if not os.path.isdir("/".join(out_path.split("/")[:-2])):
                    os.mkdir("/".join(out_path.split("/")[:-2]))
                if not os.path.isdir(out_path):
                    os.mkdir(out_path)
                with open(out_path + "data", "w+") as f:
                    f.write(json.dumps(output_accs))
                with open(out_path + "logo", "w+") as f:
                    f.write(return_dict_acc[similar_account][3])
        print(similar_accounts)

big_analysis(sys.argv[1])