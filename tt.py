from bs4 import BeautifulSoup
import requests, json

link = 'https://stackoverflow.com/jobs?med=site-ui&ref=jobs-tab&sort=p'
r = requests.get(link)
soup = BeautifulSoup(r.text, 'html.parser')

s = soup.find('script', type='application/ld+json')

# JUST THIS
json = json.loads(s.string)
breakpoint()