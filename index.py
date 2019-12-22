from lxml import html,etree
import requests

script = """
    headers = {
        ['User-Agent']='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    splash:set_custom_headers(headers)
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    return splash:html()
"""
resp = requests.post(url="http://192.168.99.100:8050/run",json={
    'lua_source':script,
    'url':"https://uk.flightaware.com/live/flight/HOP1319"
})

with open('index.html', 'wb') as f:
    f.write(resp.content)