# import time, datetime, os, csv
# import  os, datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
# from tqdm import tqdm
# from icecream import ic 
from datetime import datetime


baseurl='https://andnet.ro/dispecerat/'
download_folder = 'data/raw/'

req = Request(baseurl , headers={'User-Agent': 'Mozilla/5.0'}) #approach url cere pagina html

try:
  webpage = urlopen(req).read()  #approach url obtine pagina hmtl in text (?)
except:
  print('error downloading ' + baseurl)
  quit()
soup = bs(webpage, "html.parser") #parseaza html text si il aseaza frumos in pagina
content_wrapper = soup.find('div', class_ = 'categories-index')

carneWrapper = soup.find(id="pgprinc")
# div2 = soup.find("div", {"id": "pgprinc"})

carne = carneWrapper.findChildren("div", recursive=False)
# ic(carne)
# build output name
with open(download_folder + datetime.today().strftime('%Y-%m-%d_%H%M') + "-dispecerat.html", "w") as file:
    file.write(str(carne)) 
with open(download_folder + "_last.html", "w") as file:
    file.write(str(carne)) 