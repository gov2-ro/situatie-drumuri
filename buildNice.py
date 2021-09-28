import os, json
from datetime import datetime

# import time, datetime, os, json, csv
from icecream import ic
import pandas as pd

from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor


sourceJson = "data/json/latest.json"
rez = "data/rez.html"
mbaseurl='https://andnet.ro/dispecerat/dispecerat.php'
with open(sourceJson) as json_file:
    data = json.load(json_file)
    # breakpoint()
    # ic(data)
    xroads = data["data"]["4"]["data"]

# breakpoint()
for p in xroads:
    # ic(p)
    # xx = xroads[p]
    # print(type(xx))
    # print(  'NR. CRT.:' + p['NR. CRT.']['text'] + 'Indicativ drum:' + p['Indicativ drum']['text'] + 'De la km:' + p['De la km']['text'] + 'Pana la km:' + p['Pana la km']['text'] + 'De la data:' + p['De la data']['text'] + 'Pana la data:' + p['Pana la data']['text'] + 'Intre localitatile:' + p['Intre localitatile']['text'] + 'Cauza:' + p['Cauza']['text'] + 'Masuri de remediere:' + p['Masuri de remediere']['text']  )
    # breakpoint()

    # NOW PARSE
    zurl = mbaseurl + '?indice_drum=' +  p['Indicativ drum']['text'] + '&dela=' +p['De la km']['text'] + '&panala=' + p['Pana la km']['text'] + '&acces=3614'
    print(zurl)
    req = Request(zurl, headers={'User-Agent': 'Mozilla/5.0'}) #approach url cere pagina html

    try:
        webpage = urlopen(req).read()  #approach url obtine pagina hmtl in text (?)
    except:
        print('error downloading ' + mbaseurl)
        quit()
    soup = bs(webpage, "html.parser") #parseaza html text si il aseaza frumos in pagina
    zcript = soup.select('body script')
    # breakpoint()
    zzcript = zcript[0].contents[0].string.replace("\r\n",' ').replace("\t", ' ')

    # FIXME: 
    # https://www.py4u.net/discuss/260094
    # https://www.py4u.net/discuss/219208
    # https://newbedev.com/extract-content-of-script-with-beautifulsoup
    breakpoint()
    # print(zzcript)
    # exit()
    # json = json.loads(zzcript)
    # parse js
    # parser = Parser()
    # tree = parser.parse(zcript)
    # fields = {getattr(node.left, 'value', ''): getattr(node.right, 'value', '')
    #         for node in nodevisitor.visit(tree)
    #         if isinstance(node, ast.Assign)}

    # ic(fields)
   
