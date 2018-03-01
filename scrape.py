import requests
import re
import scrapy
import pandas as pd
import time
import logging

from time import gmtime, strftime
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup

logging.basicConfig(filename='scrape'+strftime("%Y%m%d_%H%M", gmtime())+'.log',level=logging.DEBUG)

#how deep to scrape in a reddit
start = 25
end = 2501

start_sr = 25
end_sr = 201

#whether to scrape subreddits
scrape_subreddits = True

#set search strings for easy changes here
title_string = '.*<a class=\"title.*?>(.*?)</a>'
id_string = '.*id=\"(thing_[^\s]+)"'
rank_string = ".*data-rank=\"([0-9]+)\""
source_string = ".*data-subreddit-prefixed=\"(.*?)\""
url_string = '.*data-permalink=\"(.*?)\s'
author_string = ".*data-author=\"(.*?)\""
time_string = ".*\"live-timestamp\">(.*?)</time>"
post_string = ".*datetime=\"(.*?)\""
comments_string = ".*data-comments-count=\"(.*?)\""
score_string = ".*data-score=\"(.*?)\""
xpost_string = ".*data-num-crossposts=\"(.*?)\""
domain_string = ".*<a href=\"/domain/(.*?)/\""

def scraping(item):
    subreddit = {}

    text = item.extract()

    subreddit['scrape_source'] = root_url
    subreddit['scrape_time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    ti = re.match(title_string,text)
    if ti:
        subreddit['title'] = ti.group(1)
    
    m = re.match(id_string,text)
    if m:
        subreddit['id'] = m.group(1)

    r = re.match(rank_string,text)
    if r:
        subreddit['rank'] = r.group(1)

    s = re.match(source_string,text)
    if s:
        subreddit['source'] = s.group(1)

    u = re.match(url_string,text)
    if url:
        subreddit['url'] = u.group(1)

    a = re.match(author_string,text)
    if a:
        subreddit['author'] = a.group(1)

    t = re.match(time_string,text)
    if t:
        subreddit['time_elapsed'] = t.group(1)

    p = re.match(post_string,text)
    if p:
        subreddit['post_time'] = p.group(1)

    c = re.match(comments_string,text)
    if c:
        subreddit['comments'] = c.group(1)

    ds = re.match(score_string,text)
    if ds:
        subreddit['score'] = ds.group(1)

    x = re.match(xpost_string,text)
    if x:
        subreddit['xposts'] = x.group(1)

    d = re.match(domain_string,text)
    if d:
        subreddit['domain'] = d.group(1)

    return subreddit

def RetrieveAndScrape(url):
    headers = {
    'User-Agent': 'Schillawski-GA-Project',
    'From': 'mjschillawski@gmail.com'
    }

    try:   
        # Establishing the connection to the web page:
        response = requests.get(url,headers=headers)

        # You can use status codes to understand how the target server responds to your request.
        # Ex., 200 = OK, 400 = Bad Request, 403 = Forbidden, 404 = Not Found.
        logging.info('scraping: %s',url)
        logging.info('response: %s',response.status_code)

        # Pull the HTML string out of requests and convert it to a Python string.
        html = response.text

        #parse top-level reddits
        post_list = Selector(text=html).xpath("//*[contains(@id,'thing')]")

        reddits = []

        for post in post_list:
            subreddit = scraping(post)
            reddits.append(subreddit)     
 
        return reddits

    except:
        logging.warning('Failed to scrape %s',url)

#top-level scrape
logging.info('Top level scrape began at:')
logging.info(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
#https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python

root_url = "https://www.reddit.com/r/all"
url = root_url

try:
    reddits = RetrieveAndScrape(url)
except:
    logging.warning('failed to append %s to list',url)
    retrieved = pd.DataFrame(reddits)
    retrieved.to_csv('results_'+strftime("%Y%m%d_%H%M", gmtime())+'.csv')
    logging.warning('data exported')

#retrieve and parse top-level deeper pages
for i in range(start,end,25):
    time.sleep(1)
    
    if reddits[-1]['rank']==str(i):
        #increment root_url by ID and rank
        new_index = (reddits[-1]['id'].replace('thing_',''))
        url = root_url+'?count='+str(i)+'&after='+new_index

        try:
            result = RetrieveAndScrape(url)
            reddits = reddits + result
        except:
            logging.warning('failed to append %s to list',url)
            retrieved = pd.DataFrame(reddits)
            retrieved.to_csv('results_'+strftime("%Y%m%d_%H%M", gmtime())+'.csv')
            logging.warning('data exported')

#Export top-level results to dataframe
retrieved = pd.DataFrame(reddits)

#get setted list of all sub-reddits drawn to top page
subreddit_scrape_list = list(set(retrieved['source']))
logging.info('Scraping: '+str(len(subreddit_scrape_list))+' subreddits')

#clear holding space for subreddit results
reddits = []

for index,sr in enumerate(subreddit_scrape_list):
    subreddit_scrape_list[index] = 'https://www.reddit.com/'+sr

if scrape_subreddits==True:
    #retrieve and parse sub-reddits and deeper pages
    for sr in subreddit_scrape_list:
        time.sleep(1)
        
        #set root_url to subreddit
        root_url = sr
        url = root_url    

        try:
            result = RetrieveAndScrape(url)
            reddits = reddits + result
        except:
            logging.warning('failed to append %s to list',url)
            subreddits = pd.DataFrame.from_dict(reddits)    
            retrieved = retrieved.append(subreddits,ignore_index=True)
            retrieved.to_csv('results_'+strftime("%Y%m%d_%H%M", gmtime())+'.csv')
            logging.warning('data exported')
        for i in range(start_sr,end_sr,25):
            time.sleep(1)

            if reddits[-1]['rank']==str(i):
                #increment url by ID and rank
                new_index = (reddits[-1]['id'].replace('thing_',''))
                url = root_url+'?count='+str(i)+'&after='+new_index

                # Establishing the connection to the web page:
                try:
                    result = RetrieveAndScrape(url)
                    reddits = reddits + result
                except:
                    logging.warning('failed to append %s to list',url)
                    subreddits = pd.DataFrame.from_dict(reddits)    
                    retrieved = retrieved.append(subreddits,ignore_index=True)
                    retrieved.to_csv('results_'+strftime("%Y%m%d_%H%M", gmtime())+'.csv')
                    logging.warning('data exported')

    #export results
    subreddits = pd.DataFrame.from_dict(reddits)

    retrieved = retrieved.append(subreddits,ignore_index=True)
    
else:
    pass
retrieved.to_csv('results_'+strftime("%Y%m%d_%H%M", gmtime())+'.csv')

logging.info('Scrape finished')
#end
