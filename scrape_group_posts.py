import requests
import json
from wordcloud import WordCloud

def add_counters(master, new):
    dnew = dict(new)
    for k in dnew:
        if k not in master.keys():
            master[k] = dnew[k]
        else:
            master[k] += dnew[k]

def update_counter(wc, s, ctr):
    add_counters(ctr, wc.process_text(s))
    return ctr

def do_comments(id):
    accesskey = open('accesskey','r').read()
    _url = "https://graph.facebook.com/v2.8/$ID/comments?access_token=_at_"
    __url = "https://graph.facebook.com/v2.8/$ID/comments?after=$F&access_token=$AT"
    _url=_url.replace('$ID',id)
    __url = __url.replace('$ID', id)
    __url = __url.replace('$AT',accesskey)
    _url=_url.replace('_at_',accesskey)

    s = ''

    try:
        #while True:
        r = requests.get(_url)
        data = json.loads(r.text)
        print(data.keys())
        for comment in data['data']:
            try:
                pass
                #print('c:', comment['message'])
                s += comment['message'] + '\n'
            except KeyError:
                pass
        _url = __url.replace('$F',data['paging']['cursors']['after'])
        print(_url)
        r = requests.get(_url)
    except KeyError:
        return s
    return s

accesskey = open('accesskey','r').read()
groupid = open('groupid','r').read()
_url = "https://graph.facebook.com/v2.8/__/feed?access_token=_at_"
_url=_url.replace('__',groupid)
_url=_url.replace('_at_',accesskey)
ctr = {}
wc = WordCloud(height=400, width=800)

pages = 10

while pages:
    data = requests.get(_url).text
    data = json.loads(data)
    for post in data['data']:
        try:
            update_counter(wc, post['message']+'\n'+do_comments(post['id']), ctr)
        except KeyError:
            pass
    try:
        _url = data['paging']['next']
        pages -= 1
        print("Next page.", pages,"more pages to go.")
    except KeyError:
        print(data)
        break
    break

wc.generate_from_frequencies(ctr.items()).to_file('out.png')
