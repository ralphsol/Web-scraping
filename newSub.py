'''This script could be used to extract the difference in
the share prices and the futures price of the top 20 companies
at the NSE. The prices are taken from NDTV Profit'''

import urllib2
import re
from bs4 import BeautifulSoup

def remTag(string):
    string = str(string)[1:-1]
    count = 1
    res = ""
    for c in string:
        if count == 0 and c not in {" ", "<", ">"}:
            res += c
        if c == ">":
            count -= 1 
        elif c == "<":
            count += 1 
    return res[:-1]

companies = ["http://profit.ndtv.com/stock/tata-consultancy-services-ltd_tcs",
            "http://profit.ndtv.com/stock/reliance-industries-ltd_reliance",
            "http://profit.ndtv.com/stock/itc-ltd_itc",
            "http://profit.ndtv.com/stock/hdfc-bank-ltd_hdfcbank",
            "http://profit.ndtv.com/stock/infosys-ltd_infy",
            "http://profit.ndtv.com/stock/coal-india-ltd_coalindia",
            "http://profit.ndtv.com/stock/oil-&-natural-gas-corporation-ltd_ongc",
            "http://profit.ndtv.com/stock/state-bank-of-india_sbin",
            "http://profit.ndtv.com/stock/housing-development-finance-corporation-ltd_hdfc",
            "http://profit.ndtv.com/stock/sun-pharmaceutical-industries-ltd_sunpharma",
            "http://profit.ndtv.com/stock/hindustan-unilever-ltd_hindunilvr",
            "http://profit.ndtv.com/stock/icici-bank-ltd_icicibank",
            "http://profit.ndtv.com/stock/wipro-ltd_wipro",
            "http://profit.ndtv.com/stock/maruti-suzuki-india-ltd_maruti",
            "http://profit.ndtv.com/stock/bharti-airtel-ltd_bhartiartl",
            "http://profit.ndtv.com/stock/larsen-&-toubro-ltd_lt",
            "http://profit.ndtv.com/stock/kotak-mahindra-bank-ltd_kotakbank",
            "http://profit.ndtv.com/stock/hcl-technologies-ltd_hcltech",
            "http://profit.ndtv.com/stock/tata-motors-ltd_tatamotors",
            "http://profit.ndtv.com/stock/axis-bank-ltd_axisbank",
            "http://profit.ndtv.com/stock/ntpc-ltd_ntpc",
            "http://profit.ndtv.com/stock/indian-oil-corporation-ltd_ioc",
            "http://profit.ndtv.com/stock/lupin-ltd_lupin",
            "http://profit.ndtv.com/stock/asian-paints-ltd_asianpaint"]

##wiki = "http://profit.ndtv.com/stock/reliance-industries-ltd_reliance"
##wiki = "http://profit.ndtv.com/stock/oil-&-natural-gas-corporation-ltd_ongc"
final = []
for wiki in companies:
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page, "html5lib")
    right_table = soup.find('table', id = 'faoSummaryTable')
    count = 0
    for row in right_table.findAll("tr"):
        cells = row.findAll('td')
        states = row.findAll('th')
        if count == 1:
            data = cells[2]
            finVal = float(remTag(data).replace(',', ''))
        count += 1
    currVal = float(remTag(soup.find('span', class_ = "senx-up-down")).replace(',', ''))
    ##print currVal 
    ##print finVal
    ##print wiki[29:]
    ##print round(max(finVal/currVal, currVal/finVal), 3)
    final.append((round(max(finVal/currVal, currVal/finVal), 3), wiki[29:])) 

final.sort(reverse = True)
for val in final:
    print val[1] + " : " + str(val[0])
