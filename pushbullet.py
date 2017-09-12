import asyncio
import aiohttp


ENDPOINT = 'https://api.pushbullet.com'


class Pushbullet:

    def __init__(self, token):
        self.token = token

    async def do_request(self, method, path, data=None):
        headers = {
            'Access-Token': self.token,
        }

        url = f'{ENDPOINT}/v2{path}'

        async with aiohttp.ClientSession() as session:
            method = getattr(session, method)

            async with method(url, headers=headers, json=data) as response:
                return await response.json()


    async def post(self, path, data=None):
        return await self.do_request('post', path, data=data)


    async def get(self, path):
        return await self.do_request('get', path)

    async def push_note(self, title, body):
        data = {
            'type': 'note',
            'title': title,
            'body': body
        }

        return await self.post('/pushes', data)
