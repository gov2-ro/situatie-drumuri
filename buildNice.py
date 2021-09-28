import os, json, re, time
from datetime import datetime

# import time, datetime, os, json, csv
from icecream import ic
import pandas as pd
import demjson
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
import ast
# import numpy as np
from tqdm import tqdm
# from slimit import ast
# from slimit.parser import Parser
# from slimit.visitors import nodevisitor


sourceJson = "data/json/latest.json"
outputJson = "data/rez.json"
mbaseurl = "https://andnet.ro/dispecerat/dispecerat.php"
niceJson = []

def swapCoords(x):
    out = []
    for iter in x:
        if isinstance(iter, list):
            out.append(swapCoords(iter))
        else:
            return [x[1], x[0]]
    return out

def getSection(xroads):

    rez = {"title": xroads["title"], "type": xroads["type"], "roads": []}
    rsize = len(xroads['data'])
    pbar = tqdm(total=rsize)
    ii = 0
    for p in xroads["data"]:
        ii += 1
        # if ii >=4:
        #     break
        item = {
            "indice_drum": p["Indicativ drum"]["text"],
            "dela": p["De la km"]["text"],
            "panala": p["Pana la km"]["text"],
            "acces": 3614,
        }
        # ic(p)
        # xx = xroads[p]
        # print(type(xx))
        # print(  'NR. CRT.:' + p['NR. CRT.']['text'] + 'Indicativ drum:' + p['Indicativ drum']['text'] + 'De la km:' + p['De la km']['text'] + 'Pana la km:' + p['Pana la km']['text'] + 'De la data:' + p['De la data']['text'] + 'Pana la data:' + p['Pana la data']['text'] + 'Intre localitatile:' + p['Intre localitatile']['text'] + 'Cauza:' + p['Cauza']['text'] + 'Masuri de remediere:' + p['Masuri de remediere']['text']  )
        # breakpoint()

        # NOW PARSE GIS
        zurl = (
            mbaseurl
            + "?indice_drum="
            + p["Indicativ drum"]["text"]
            + "&dela="
            + p["De la km"]["text"]
            + "&panala="
            + p["Pana la km"]["text"]
            + "&acces=3614"
        )
        # zurl = "http://zx/gov2/dispecerat-cnadr/data/raw/sample-path.html"
        tqdm.write('>> ' + str(ii) + ' / ' + str(rsize) + ' - ' + zurl)
        req = Request(
            zurl, headers={"User-Agent": "Mozilla/5.0"}
        )  # approach url cere pagina html

        try:
            webpage = urlopen(req).read()  # approach url obtine pagina hmtl in text (?)
        except:
            print("error downloading " + mbaseurl)
            quit()
        soup = bs(
            webpage, "html.parser"
        )  # parseaza html text si il aseaza frumos in pagina
        zcript = soup.select("body script")
        zzcript = (
            zcript[0]
            .contents[0]
            .string.replace("\t", "")
            .replace("\n", "")
            .replace(",}", "}")
            .replace(",]", "]")
        )
        strx = "{" + zzcript + "}"
        json_data = ast.literal_eval(json.dumps(strx))

        match1 = (
            re.search(r"data=\[{.*data2=", json_data, re.DOTALL)
            .group(0)
            .replace("data=", "")
            .replace(";var data2", "")
        )
        m1 = match1[:-1]  # remove last char from string
        obj1 = demjson.decode(m1)[0]
        item['Desc']=obj1['Desc']
        # FIXME: reverse coords
        krds = obj1['coords']
        xkrds=[]
        # breakpoint()
        for feature in krds:
            # feature  = 
            xkrds.append(swapCoords(feature))
        # breakpoint()
        item['coords']=xkrds
        # obj1['Desc']
        # obj1['coords']
        # breakpoint()
        # not needed
        # match2 = re.search(r'data_polygon=\[{.*function addPointGeom_polygon', json_data, re.DOTALL).group(0).replace('data_polygon=','').replace(';function addPointGeom_polygon','')
        rez['roads'].append(item)
        pbar.update(1)
        time.sleep(3)
    return rez 
tqdm.write('start')    
with open(sourceJson) as json_file:
    data = json.load(json_file)
    # breakpoint()
    # ic(data)
    # TODO: loop for all
    zroads = data["data"]["4"]
    niceJson.append(getSection(zroads))
    # breakpoint()

with open(outputJson, 'w') as outfile:
    json.dump(niceJson, outfile)

tqdm.write('done')