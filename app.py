import requests
from lxml import html
import pprint
import click


script = '''
    headers = {
        ['Accept-Language'] = 'en-US,en;q=0.9,fr-DZ;q=0.8,fr;q=0.7,ar;q=0.6',
        ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    splash:set_custom_headers(headers)
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    return splash:html()
'''

@click.command()
@click.option('--flightcode', default='DLH1052', help='Post a valid flight code to get the upcoming flights')
def scrape(flightcode):
    resp = requests.post(url='http://192.168.99.100:8050/run', json={
        'lua_source': script,
        'url': f'https://flightaware.com/live/flight/{flightcode}'
    })

    #tree
    tree = html.fromstring(html=resp.content)
    
    #scraping past flights
    past_flights = tree.xpath("//div[@data-type='upcoming']")
    for past_flight in past_flights:
        p = {
            #The date XPath expression will return two text elements,
            #therefor we need to join them.
            'Date': ' '.join(past_flight.xpath(".//div[1]/span/em/text()")),
            'Departure time': past_flight.xpath(".//div[2]/div/div/span/em/span/text()")[0],
            'Departure airport': past_flight.xpath(".//div[2]/div/div/span[2]/a/@data-tip")[0],
            'Arrival time': past_flight.xpath(".//div[3]/div/div/span/em/span[@class='noWrapTime']/text()")[0],
            'Arrival airpot': past_flight.xpath(".//div[3]/div/div/span[2]/a/@data-tip")[0],
            'Aircraft': past_flight.xpath(".//div[4]/span/@data-tip")[0],
            'Duration': past_flight.xpath(".//div[5]/em/text()")[0].strip()
        }
        pprint.pprint(p)


if __name__ == '__main__':
    scrape()
