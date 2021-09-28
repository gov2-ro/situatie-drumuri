import os, json, re
from datetime import datetime
# import time, datetime, os, json, csv
from icecream import ic
import pandas as pd
import demjson
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
import ast

# from slimit import ast
# from slimit.parser import Parser
# from slimit.visitors import nodevisitor


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
    zurl = 'http://zx/gov2/dispecerat-cnadr/data/raw/sample-path.html'
    print(zurl)
    req = Request(zurl, headers={'User-Agent': 'Mozilla/5.0'}) #approach url cere pagina html

    try:
        webpage = urlopen(req).read()  #approach url obtine pagina hmtl in text (?)
    except:
        print('error downloading ' + mbaseurl)
        quit()
    soup = bs(webpage, "html.parser") #parseaza html text si il aseaza frumos in pagina
    zcript = soup.select('body script')
    zzcript = zcript[0].contents[0].string.replace('\t','').replace('\n','').replace(',}','}').replace(',]',']')
    strx = '{' + zzcript + '}'
    json_data = ast.literal_eval(json.dumps(strx))

    match1 = re.search(r'data=\[{.*data2=', json_data, re.DOTALL).group(0).replace('data=','').replace(';var data2','')
    m1 = match1[:-1] #remove last char from string
    obj1 = demjson.decode(m1)[0]
    # obj1['Desc']
    # obj1['coords']
    # breakpoint()

    match2 = re.search(r'data_polygon=\[{.*function addPointGeom_polygon', json_data, re.DOTALL).group(0).replace('data_polygon=','').replace(';function addPointGeom_polygon','')
    # breakpoint()
    m2 = match2
    obj2 = demjson.decode(m2)[0]
    # obj2['coords']
    breakpoint()
