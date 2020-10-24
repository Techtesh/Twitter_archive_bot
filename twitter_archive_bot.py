# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:19:04 2020

@author: Hitesh
"""
import time
import selenium
import tweepy
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


#put your keys here
CONSUMER_KEY=""
CONSUMER_SECRET=""
ACCESS_KEY=""
ACCESS_SECRET=""

#function to create archive and fetch the link
def pager(address,val):
    fop=0
    driver_path="C:/Users/Hitesh/Downloads/chromedriver.exe"
    driver = webdriver.Chrome(driver_path)
    """
    #PUT OPTIONS HERE FOR HEADLESS OPERATIONS
    """
    driver.get(address)
    #avoids archiving twitter and youtube links 
    if ("Twitter" not in driver.title and"youtube" not in driver.current_url)or val:
        print("@"*10,driver.title)
        if ("twitter" not in driver.current_url)or val:
            
            link=driver.current_url
            print("ARCHIVING:",link)#start of making an archive
            """ MAKE ARCHIVE  """
            driver.get("https://web.archive.org/save")#open web archive page
            #get the correct selection box
            try:
                    field1=driver.find_element_by_id("web-save-url-input")
            except:
                try:
                    field1=driver.find_element_by_class_name("form-control web-save-url-input web_input web_text")
                except:
                    print("facing error")
                    time.sleep(25)
                    print("solving error")
                    field1=driver.find_element_by_class_name("form-control web-save-url-input web_input web_text")
            #send data and "ENTER" to the correct field        
            field1.send_keys(link)
            field1.send_keys(Keys.ENTER)
            time.sleep(50)
            try:
                op=driver.find_element_by_partial_link_text("/web/")
            except:
                time.sleep(125)
                op=driver.find_element_by_partial_link_text("/web/")
            links = []
            eles = driver.find_elements_by_xpath("//*[@href]")
            #get the archive link after the web page is saved
            for elem in eles:#
                url = elem.get_attribute('href')
                if "/web/"in url:
                    #print(url)
                    fop=url
                    links.append(url) 
            print("ARCHIVE AT:",fop)
            return fop
                
        else:
            print("TWITTER/Youtube LINK NOT ARCHIVING")
            return 0
        
    else:
        print("!"*10,driver.title)
        return 0
    return 0
    
TWEET_INIT=0    

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api=tweepy.API(auth)
#get all tweets
public_tweets = api.home_timeline()
#set val as true to archive the 1st link irrespective of its type ..
val=True
for tweet in public_tweets:
    print(f"{tweet.id}    : {tweet.text}")
    if tweet.text[:2]=="RT":
        pass
        print("#"*10,"RETWEET FROM SOMEONE ELSE")
    #print(tweet.id,"from",tweet.author.screen_name,"\t",tweet.text,"\n")
    
    
    
    #tweet.user gives all info about user
    #if the tweet has a link embedded it is usually shortened 
    if "http" in tweet.text and "t.co"  in tweet.text:#alternatively if "https://t.co" in tweet.text:
        print("#"*10,"LINK ")
        #isolate link from the remaining tweet
        i=str(tweet.text).index("http")
        print(tweet.text[i:]) 
        link=tweet.text[i:]
        #send request for archive and get archived link as the response (fop)
        #this ensures same link is not archived 
        if tweet.id>TWEET_INIT:
            try:
                fop=pager(link,val)
                val=False
                if fop!=0:
                    reply="@"+tweet.author.screen_name+" sorry working on a bot . Archive of this post can be found at "+fop
                    print(reply)
                    api.update_status(reply,in_reply_to_status_id=tweet.id,auto_populate_reply_metadata=True)
                    print("message sent to ",reply[:-(22+len(fop))])
            except:
                print("SKIPPING DUE TO ERROR NOTE",link)
                """
                Expansion note Write All links that were not archived to a .txt file
                """
            TWEET_INIT=tweet.id
    print("\n\n")
    
