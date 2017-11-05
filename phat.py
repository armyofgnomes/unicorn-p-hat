import time
#import colorsys
import yaml
from TwitterAPI import TwitterAPI

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

twitter_cfg = cfg['twitter']

api = TwitterAPI(twitter_cfg['api_key'], twitter_cfg['api_secret'], twitter_cfg['access_token'], twitter_cfg['access_token_secret'])
terms = twitter_cfg['tracking_terms']

count = 0
skip = 0
r = api.request('statuses/filter', {'track': terms})
for item in r:
  if 'text' in item:
    count += 1
  elif 'limit' in item:
    skip = item['limit'].get('track')
    print('*** SKIPPED %d TWEETS' % skip)
  elif 'disconnect' in item:
    print('[disconnect] %s' % item['disconnect'].get('reason'))
    break
  print(count+skip);
