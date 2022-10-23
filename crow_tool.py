import random
import time
import multiprocessing
import os
from tf import tf
import similarity

related_accounts = {}
manager = multiprocessing.Manager()
return_dict = manager.dict()
tweets = {}
jobs = []

accs = ["elonmusk", "SJobs_Stories", "SteveJobsFilm", "SteveJobsFeed", "romscot", "aaSteveJobs.Steve", "forealstevejobs", "WalterIsaacson", "Tulane", "NolanBushnell", "Moxyio", "champtgram", "champsonlypass"]
filter_quality = .5

if __name__ == "__main__":
    for acc in accs:
        try:
            p = multiprocessing.Process(target=similarity.get_user_tweets, args=(acc, return_dict))
            jobs.append(p)
            p.start()
        except:
            print("Getting tweets Failed!\n\n")
    
    for proc in jobs:
        proc.join()

    for i in return_dict:
        tweets[i] = ' '.join(return_dict[i][0])

    print("-"*30)

    if len(tweets.keys()) < 2:
        print("Not enough ACCs")
        exit()

    ref, data = tf(tweets)

    for ind, ary in enumerate(ref):
        for i, el in enumerate(ary):
            if i != ind:
                try:
                    el += 10 * ( 1 / similarity.get_daily_time(return_dict[accs[ind]][1], return_dict[accs[i]][1]) )
                    el += 10 * ( 1 / similarity.compare_media(return_dict[accs[ind]][2], return_dict[accs[i]][2]) )
                except:
                    pass

                if el >= filter_quality:
                    related_accounts[ind] = None
                    related_accounts[i] = None
                    break

    accounts = []
    x = 0
    for acc in tweets:
        if x in related_accounts:
            accounts.append(acc)
        x += 1

    print(accounts)