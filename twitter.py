import os
import asyncio

from peony import PeonyClient
from peony import events
from pushbullet import Pushbullet

loop = asyncio.get_event_loop()

PUSHBULLET_TOKEN = os.getenv('PUSHBULLET_TOKEN')

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
ALERTS = os.getenv('ALERTS', '').split(',')


client = PeonyClient(consumer_key=CONSUMER_KEY,
                     consumer_secret=CONSUMER_SECRET,
                     access_token=ACCESS_TOKEN,
                     access_token_secret=ACCESS_TOKEN_SECRET)

pushbullet = Pushbullet(PUSHBULLET_TOKEN)


async def send(alert, tweet_text):
    title = f'New {alert} alert'
    body = tweet.text

    await pushbullet.push_note(title, body)

async def process(tweet):
    print(f'Got tweet {tweet}')

    for alert in ALERTS:
        if alert in tweet.text:
            print(f'Alerting you about {alert} - {tweet.text}')
            await send(alert, tweet.text)

async def track():
    req = client.stream.statuses.filter.post(follow="1344755923")
    print(f'Setup {req} with alerts {ALERTS}')

    async with req as stream:
        async for tweet in stream:
            if events.tweet(tweet):
                await process(tweet)


try:
    loop.run_until_complete(track())
except KeyboardInterrupt:
    print('Closing')
finally:
    loop.close()

