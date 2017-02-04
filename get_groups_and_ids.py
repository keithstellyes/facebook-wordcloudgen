import requests
import json

_url = "https://graph.facebook.com/v2.8/me/groups?access_token={}"

accesskey = open('accesskey','r').read()

_url=_url.format(accesskey)

data = requests.get(_url).text
data = json.loads(data)

for g in data['data']:
    print('Name: {} ID: {}'.format(g['name'], g['id']))
