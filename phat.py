import time
import colorsys
import yaml
import unicornhat as uh
from TwitterAPI import TwitterAPI

# Configure pHat
uh.set_layout(uh.PHAT)
uh.brightness(0.5)

# Open Twitter configuration
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

twitter_cfg = cfg['twitter']

api = TwitterAPI(twitter_cfg['api_key'], twitter_cfg['api_secret'], twitter_cfg['access_token'], twitter_cfg['access_token_secret'])
terms = twitter_cfg['tracking_terms']

count = 0
skip = 0
hue = 0.0
latest_tweet_interval = time.time()
tweet_interval_count = 0
r = api.request('statuses/filter', {'track': terms})

for item in r:
  if 'text' in item:
    count += 1
    tweet_interval_count += 1
    if time.time() >= latest_tweet_interval + 30.0:
        hue = tweet_interval_count
        latest_tweet_interval = time.time()
        tweet_interval_count = 0
    if hue > 270:
        hue = 270.0
    h = hue / 360.0
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
    for x in range(8):
        for y in range(4):
            uh.set_pixel(x, y, r, g, b)
        uh.show()
  elif 'limit' in item:
    skip = item['limit'].get('track')
    print('*** SKIPPED %d TWEETS' % skip)
  elif 'disconnect' in item:
    print('[disconnect] %s' % item['disconnect'].get('reason'))
    break
  print(count+skip);

