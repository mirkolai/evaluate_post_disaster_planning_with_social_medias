__author__ = 'mirko'
import sys
import time
import oauth2 as oauth
import json
import config as cfg
import MySQLdb

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
clientTwitter = oauth.Client(consumer, access_token)

cur.execute("SELECT id, json FROM tweet_weather_phenomena")
tweets = cur.fetchall()

for tweet in tweets:
    tweet_id=tweet[0]
    tweet_json=tweet[1]
    codes=None
    jsonTweet=json.loads(tweet[1])
    if jsonTweet['place']!=None:
        place_id=jsonTweet['place']['id']

        cur.execute("SELECT id, json FROM twitter_places where id=%s",(place_id))
        results = cur.fetchone()
        if results!=None:
            if '174368:admin_order_id' in json.loads(results[1])['attributes']:
                codes=json.loads(results[1])['attributes']['174368:admin_order_id']

        else:
            place_endpoint = "https://api.twitter.com/1.1/geo/id/"+place_id+".json"
            response, data = clientTwitter.request(place_endpoint)

            if response['status']=='200':
                if int(response['x-rate-limit-remaining'])<2:
                    print 'Reverse Geocoding: wait '+str( int(response['x-rate-limit-reset']) - int(time.time()) )+' seconds'
                    time.sleep(int(response['x-rate-limit-reset'])-int(time.time()))

                result=json.loads(data)
                print result
                if '174368:admin_order_id' in result['attributes']:
                    codes = result['attributes']['174368:admin_order_id']

                    cur.execute("INSERT twitter_places (id,json) "
                            "VALUES (%s,%s) "
                            "on duplicate key update id=id",
                            (place_id,data))
                    db.commit()

                print ': wait 60 seconds'
                time.sleep((15*60)/int(response['x-rate-limit-limit']))

        if codes!=None:
            #example ITA:07::::::010:010025
            if codes[0:3]=='ITA':
                admin_order_1=codes[4:6]
                admin_order_2=codes[12:15]
                admin_order_3=codes[16:]
                print admin_order_1,admin_order_2,admin_order_3
                cur.execute("UPDATE tweet_weather_phenomena "
                            "SET admin_order_1=%s,"
                            "admin_order_2=%s,"
                            "admin_order_3=%s WHERE id=%s",
                            (admin_order_1,admin_order_2,admin_order_3,tweet_id))
                db.commit()