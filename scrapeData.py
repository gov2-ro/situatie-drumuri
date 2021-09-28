import   os, json
from datetime import datetime
# import time, datetime, os, json, csv
from icecream import ic 
# from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd

cachedFile = "data/raw/_last.html"
outfolder = "data/json/"


def extract_tablez(table_tag):
    """ Extract data from a table, return the column headers and the table rows"""
    # https://stackoverflow.com/a/44707545/107671
    # SCRAPE: Get a table
    # table_tag = soup.find("table", {"id" : 'SeasonSplits1_dgSeason%d_ctl00' % table_id})

    # SCRAPE: Extract table column headers
    columns = [th.text for th in table_tag.findAll("th")]

    rows = []
    # SCRAPE: Extract Table Contents
    for row in table_tag.tbody.findAll("tr"):
        # look  for vizualizare
        # rows.append ([{col.text} for col in row.findAll('td')])  # Gather all columns in the row
        rrow = []
        for td in row.findAll("td"):
            # rows.append([{td.text}])
            attrz = {}
            placeholder = ''
            if td.has_attr("placeholder"):
                placeholder = td["placeholder"]
            if td.has_attr("onclick"):
                onclick = td["onclick"]
                #  if it has onclick and placeholder ok
                # get attributes
                onclickx = onclick.split("(")
                onclicky = onclickx[1].split(")")
                attrz = onclicky[0].split(",")
                
            if len(attrz):
                rrow.append({'text': td.text, 'placeholder': placeholder, 'attrz': attrz})
                # print(len(attrz))
                # breakpoint()
            else:
                rrow.append({'text': td.text, 'placeholder': placeholder})
            # if attrz:
            #   breakpoint()
        rows.append(rrow) 
        # breakpoint()

    # RETURN: [columns, rows]
    return [columns, rows]


with open(cachedFile) as fp:
    soup = bs(fp, "html.parser")
zijson = {
  'title':'',
  'data':{}
}
# gaseste titlu
# then loop through div.
carne1 = soup.findChildren("div", recursive=False)
carne = carne1[0].findChildren("div", recursive=False)
# carne = soup.select("div[class='fadeIn']")
# print(carne[0])
# print(carne1[0])
divz1 = soup.findChildren("div", recursive=False)
# title = divz1[0].select("p[class='h5']")
titlez = carne1[0].find("p", {"class": "h2"}).text
zijson['title'] = titlez
# print(divz1[0])
# karne = divz1[0].findAll('div', {'class' : 'tablerow'} )
# breakpoint()
rid = 0
for rrow in divz1[0].findAll("div", {"class": "tablerow"}):
    zijson['data'][rid] = {}
    zijson['data'][rid]['data'] = []
    zijson['data'][rid]['title'] = rrow.find("p", {"class": "h5"}).text
    #     # title = rrow.select("p[class='h5']")
    # TODO: check if nodata
    alert = rrow.find("div", {"class": "alert"})
    if alert:
        zijson['data'][rid]['titley'] = alert.text
        zijson['data'][rid]['type'] = 'alert'
    table = rrow.find("table", {"class": "table"})
    if table:
        zijson['data'][rid]['type'] = 'table'
        # df = pd.read_html(str(table))
        zitable = extract_tablez(table)
     
        # TODO: convert zitable list to json
       
        for idx, zrow in enumerate(zitable[1]): # this enumerates too much
          # zijson['data'][rid][zitable[0][rid]] = zrow
          # this assignment is broken!
        #   ic(dict(zip(zitable[0], zrow))) #FIXME - this down't work 
          zijson['data'][rid]['data'].append(dict(zip(zitable[0], zrow)))
          # print(str(rid) + ' - ' + str(idx))
          # print(idx)
          # ic(zrow)
          # breakpoint()
          # zijson['data'][rid]['data'][].append(dict(zip(zitable[0], zrow)))
    rid+=1
        
# with open(outfolder + datetime.today().strftime('%Y-%m-%d_%H%M') + ".json", 'w') as f:
with open(outfolder + datetime.today().strftime('%Y-%m-%d') + ".json", 'w') as f:
    json.dump(zijson, f, indent=4)
with open(outfolder + 'latest' + ".json", 'w') as f:
    json.dump(zijson, f, indent=4)