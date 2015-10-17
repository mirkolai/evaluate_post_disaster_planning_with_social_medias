import glob
import codecs
import os
import MySQLdb
import oauth2 as oauth
import time
import json
import config as cfg
from datetime import datetime
print os.getcwd()

db = MySQLdb.connect(host=cfg.mysql['host'], # your host, usually localhost
             user=cfg.mysql['user'], # your username
             passwd=cfg.mysql['passwd'], # your password
             db=cfg.mysql['db']) # name of the data base

cur = db.cursor()
db.set_character_set('utf8')
cur.execute('SET NAMES utf8mb4;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8mb4;')
db.commit()

CONSUMER_KEY    = cfg.twitter['CONSUMER_KEY']
CONSUMER_SECRET = cfg.twitter['CONSUMER_SECRET']
ACCESS_KEY      = cfg.twitter['ACCESS_KEY']
ACCESS_SECRET   = cfg.twitter['ACCESS_SECRET']

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

filelist = glob.glob("./data/corpus_weather_phenomena.csv")

#print filelist
print str(len(filelist))+' files to elaborate'
ids=[]

for file in filelist:
    #print file
    file_data=codecs.open(file, 'r', encoding='utf-8')

    for row in file_data:
        ids.append(row.replace("\r\n", ""))

print str(len(ids))+' ids to gather'

while len(ids) > 0:
    print str(len(ids))+' ids to gather'
    parameter = ','.join(ids[0:99]) #max 100 id per request
    endpoint ="https://api.twitter.com/1.1/statuses/lookup.json?id="+parameter
    response, data = client.request(endpoint)

    if response['status']=='200':

        if 'x-rate-limit-reset' in response and 'x-rate-limit-limit' in response and int(response['x-rate-limit-remaining'])<2:
            print 'id rescue: wait '+str( int(response['x-rate-limit-reset']) - int(time.time()) )+' seconds'
            time.sleep(int(response['x-rate-limit-reset'])-int(time.time()))

        jsonTweet=json.loads(data)
        for tweet in jsonTweet:
            #print json.dumps(tweet)
            cur.execute("INSERT tweet_weather_phenomena (id,text,"
                        "date,json) "
                        "VALUES (%s,%s,%s,%s) "
                        "on duplicate key update id=id",
                        (tweet['id'],tweet['text'],
                         datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime("%Y-%m-%d %H:%M:%S"),json.dumps(tweet)))
            db.commit()

        ids[0:99] =[]

        if 'x-rate-limit-limit' in response:
            print 'id rescue: wait '+str((15*60)/int(response['x-rate-limit-limit']))+' seconds'
            time.sleep((15*60)/int(response['x-rate-limit-limit']))
    else:
        print response['status']




db.close()