#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: pcas-git

Derive from this file for your code for Project Part 1.

demonstrates that the data collected in `twitter_gatherer_project_part_1.py` can
be parsed in using the JSON parser.  it can.
"""

#%% 
import json

with open('twitter_data_project_part1.json','r',encoding='utf8') as fin:
  data = json.load(fin)

#let's take  quick look at the data
for ii in range(0,10):
    print(data[ii])
    print('\n')

#I want to identify the associated hashtags and their counts
#hashtags are kept in the 'text' of a tweet, so first we need to collect all tweet text
#I wasn't going to make this a function, but I needed it later, so I guess it's helpful
def get_tweet_text(tweets):
    """
    Inputs
    ----------
    tweets: a list of tweets from JSON imported into python

    Returns
    -------
    A list of the tweet text.
    """
    tweet_text = []
    for ii in tweets:
        tweet_text.append(ii['text'])
    return tweet_text

#see if it works
full_tweet_text = get_tweet_text(data)
print(full_tweet_text)

#something easy to determine is how many hashtags an average tweet has
tag_count = 0
for tt in get_tweet_text(data):
    tag_count += tt.count('#')
avg_tag_count = tag_count / len(data)

#first I think we can split the text then keep only strings that start with '#'
#ok, so it turns out the hashtags get buried by newlines and emojis when splitting
#so to grab hashes we'll replace all '#' with '#$$'m then we can split by '#' and grab all tags that start with '$$', which is an unlikely sequence of characters (we could also use a loop to check if that sequence exists in the strings in our list). We can strip the $$ later
def get_hashtag_counts_from_text(tweet_list):
    """
    I think this could be useful for future tweet data, so we'll pack all these operations in a function. I realized belatedly I could grab this from the 'hashtags' dict... whoopsie
    Input: get_hashtag_counts takes in a list of tweet texts
    Output: produces a dictionary of all hashtags with associated counts in the 'text' input
    """
    tweet_split_by_hashtag = []
    hashtag_counts = {}
    for tt in tweet_list:
        tt = tt.replace('#', '#$$')
        #this is confusing, but text also comes before and after hashtags in tweets
        #so we really need to split by '#' and ' ' and '\n'. 
        #We'll just turn all spaces and newlines into '#' and still split by '#' 
        #since the actual tags will now be marked by '$$'
        tt = tt.replace(' ', '#')
        tt = tt.replace('\n', '#')
        tweet_split_by_hashtag = tt.split('#')
        #then we iterate through the list to build our dict of counts
        for ss in tweet_split_by_hashtag:
           if ss.startswith('$$'):
               ss = ss.strip('$:.,…')#alternatively we could add the '#' back in
               hashtag_counts[ss] = hashtag_counts.get(ss, 0)+1
    return(hashtag_counts)

#let's see what we have!        
hashtag_counts = get_hashtag_counts_from_text(full_tweet_text)
print(hashtag_counts)

#now we can check all the tags from our fancy new dict to see if it's the same
#as what we calculated earlier:
print('Avg Tag Count from dict:', sum(hashtag_counts.values())/300) 
#It actually matches, how about that


#time to pack everything into a dict and export to JSON
function_results = {
    'get_tweet_text' : get_tweet_text(data),
    'get_hashtag_counts_from_text' : get_hashtag_counts_from_text(get_tweet_text(data)),
    }

json_object = json.dumps(function_results)
with open("data_project_pt1_results.json", "w") as outfile:
    outfile.write(json_object)
