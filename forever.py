import urllib2
import re
from bs4 import BeautifulSoup

companies = ['tcs.BO',
            'reliance.BO',
            'itc.BO',
            'hdfcbank.BO',
            'infy.BO', 
            'coalindia.BO',
            'ongc.BO', 
            'sbin.BO', 
            'hdfc.BO',
            'sunpharma.BO',
            'HINDUNILVR.BO',
            'ICICIBANK.BO', 
            'WIPRO.BO',
            'MARUTI.BO', 
            'BHARTIARTL.BO',
            'lt.BO',
            'KOTAKBANK.BO',
            'HCLTECH.BO',
            'TATAMOTORS.BO',
            'AXISBANK.BO',
            'ntpc.BO',
            'ioc.BO',
            'lupin.BO',
            'asianpaint.BO']
final = []

for name in companies:
    wiki = "http://finance.yahoo.com/q?s=%s" % name.lower()
    page = urllib2.urlopen(wiki)
    pgtxt = page.read()
    regex = '<span id="yfs_l84_%s">(.+?)<\/span>' % name.lower()
    pattern = re.compile(regex)
    pricL = re.findall(pattern, pgtxt)
    pL =  float(str(pricL)[2:-2].replace(',', ''))
    
    wiki = "http://finance.yahoo.com/q?s=%s" % name
    page = urllib2.urlopen(wiki)
    soup = BeautifulSoup(page, "html5lib")
    ##print soup.prettify().encode('utf-8')
    right_table = soup.find('table', id='table2')
    ##print right_table
    count = 0
    for row in right_table.findAll("tr"):
        cells = row.findAll('td')
        states = row.findAll('th')
        if count == 1:
            ##print states
            dat = cells[0]
            subcell = dat.findAll('span')
            pH = float(str(subcell[1])[6:-7].replace(',', ''))
        count += 1
    final.append((round(float(pH/pL), 2), name))
    
final.sort(reverse = True)
for val in final :
    print str(val[1]).upper()[:-3] + " : " + str(val[0])
print
