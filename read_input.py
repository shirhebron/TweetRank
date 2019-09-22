import csv
import pandas as pd

def fun(filename,main_dict , user_value , tweet_text, final_tweet):
    val=0
    with open(filename, "r") as f:
        ifile = csv.reader(f, delimiter=",")
        next(ifile)
        uniqe_id=0
        for row in ifile:
            if int(row[4])>1:
                val = (3*int(row[2]) + 2*int(row[3])+int(row[4]))/6
            else:
                val=int(row[2])+int(row[3])
            main_dict[uniqe_id] = [row[0],row[1],val]
            tweet_text[uniqe_id] = row[1]
            final_tweet[uniqe_id] = [row[1],row[0]]
            uniqe_id+=1
            if row[0] in user_value:
                user_value[row[0]] = user_value[row[0]]+val
            else:
                user_value[row[0]] = val

    for i in final_tweet.items():
        total_val = 0
        user = i[1][1]
        total_val = user_value[user]
        new_list=[i[1][0],total_val,i[1][1]]
        final_tweet[i[0]].append(total_val)
    return main_dict , user_value , tweet_text, final_tweet

def read_write(filename,main_dict , user_value , tweet_text, final_tweet):
    main_dict , user_value , tweet_text, final_tweet = fun(filename,main_dict , user_value , tweet_text, final_tweet)
    print('hi')
    return final_tweet, tweet_text






