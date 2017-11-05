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
latest_tweet_time = time.time()
r = api.request('statuses/filter', {'track': terms})

for item in r:
  if 'text' in item:
    time_difference = time.time() - latest_tweet_time
    latest_tweet_time = time.time()
    count += 1
    normalized_time = 1 - time_difference
    if normalized_time < 0:
        normalized_time = 0
    hue = int((normalized_time) * 100000) % 360
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
