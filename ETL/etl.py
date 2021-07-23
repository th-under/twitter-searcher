
import pymongo
import time
from sqlalchemy import create_engine
import pandas as pd
import re
import os

# used names:
# docker container name handling mongo db: my_mongodb    
# db name: tweetsdb
# table name: ttweets
#
# commands to access mongo db:
# > show collections : shows tables (proper name is collection, not table like in sql)
# > use tweetsdb : switched to db tweetsdb
# > db.ttweets.find() : shows tweets


# intervall at which tweets should be read
INTERVALL = int(os.getenv('ETL_INTERVALL'))

def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_at_hash_http(text):
    special_pattern = re.compile('@\S+|http\S+|#\S+')
    return special_pattern.sub(r'', text)

# postgres credentials and initialization
UNAME = "postgres"
PWD = "1234"
HOST = "my_postgres"
PORT = "5432"
DB = "postgres"

pg = create_engine(f"postgresql://{UNAME}:{PWD}@{HOST}:{PORT}/{DB}")

pg.execute('''DROP TABLE IF EXISTS ttweets;''')

pg.execute('''
    CREATE TABLE IF NOT EXISTS ttweets (
    text VARCHAR(500),
    sentiment NUMERIC
    );
    ''')



# read from mongo database
conn = pymongo.MongoClient('my_mongodb')
db = conn.tweetsdb

nn_tweets = 0 # number of new tweets

while True:
    time.sleep(INTERVALL) # get tweets all INTERVALL seconds

    mongo_tweet_rows = db.ttweets.find().skip(nn_tweets);
    nn_tweets += mongo_tweet_rows.count()
    
    new_tweetsdf = pd.DataFrame()
    
    for mongo_tweet_row in mongo_tweet_rows:
        
        key, value = mongo_tweet_row['found_tweet'].items()
               
        timestamp = key[1]
        tweet = value[1]
        
        # with open('cleared_tweet','w') as debugging:
        #     debugging.write(f'{timestamp}, \n {tweet}')
            
        tweet = tweet.replace('\n', ' ').replace('\r', '')
        tweet = remove_emoji(tweet)
        tweet = remove_at_hash_http(tweet)
        
        cleared_tweet = pd.DataFrame({'Text':[tweet]}, index=[timestamp], parse_dates=True)
        
        
        new_tweetsdf = new_tweetsdf.append(cleared_tweet) 
    
    new_tweetsdf['Sentiment'] = 1.0 # adjust "1.0" here according to sentiment of tweet
        
    
    # with open('out.csv','w') as debugging:
    #     debugging.write(new_tweetsdf.to_csv())
    
    if new_tweetsdf.shape[0] > 0:
        new_tweetsdf.to_sql('ttweets', pg, if_exists='append')
        
        
        
        
# to access sql database manually use "docker.compose ps" to get docker name, then:
# "docker exec -it dockername psql -U postgres -p 5432"        

