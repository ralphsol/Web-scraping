'''This script could be used to extract the difference in
the prices of the top 20 companies at the BSE and the NSE.
The prices are taken from Yahoo Finance'''

import time
from threading import Thread
import thread
from thread import *
import threading
import urllib
import re
import datetime
import time 


final = []
companies = [
                ('tcs.bo', 'tcs.ns'),
                ('reliance.bo', 'reliance.ns'),
                ('itc.bo', 'itc.ns'),
                ('hdfcbank.bo', 'hdfcbank.ns'),
                ('infy.bo', 'infy.ns'),
                ('coalindia.bo', 'coalindia.ns'),
                ('ongc.bo', 'ongc.ns'),
                ('sbin.bo', 'sbin.ns'),
                ('hdfc.bo', 'hdfc.ns'),
                ('sunpharma.bo', 'sunpharma.ns'),
                #('HINDUNILVR.bo', 'HINDUNILVR-EQ.ns'),
                ('ICICIBANK.bo', 'ICICIBANK.ns'),
                ('WIPRO.bo', 'WIPRO.ns'),
                ('MARUTI.bo', 'MARUTI.ns'),
                #('BHARTIARTL.bo', 'BHARTIART.ns'),
                ('lt.bo', 'lt.ns'),
                ('KOTAKBANK.bo', 'KOTAKBANK.ns'),
                ('HCLTECH.bo', 'HCLTECH.ns'),
                #('TATAMOTORS.bo', 'TATAMOTOR.ns'),
                ('AXISBANK.bo', 'AXISBANK.ns'),
                ('ntpc.bo', 'ntpc.ns'),
                ('ioc.bo', 'ioc.ns'),
                ('lupin.bo', 'lupin.ns'),
                #('asianpaint.bo', 'asianpain.ns')
            ]

def find_price(name0, name1):
    name0 = name0.lower()
    name1 = name1.lower()
    #print name0[:-3]
    
    htmlfile0 = urllib.urlopen("http://finance.yahoo.com/q?s=%s" % name0)
    htmlfile1 = urllib.urlopen("http://finance.yahoo.com/q?s=%s" % name1)
    
    htmltext0 = htmlfile0.read()
    htmltext1 = htmlfile1.read()
    
    
    regex0 = '<span id="yfs_l84_%s">(.+?)<\/span>' % name0
    regex1 = '<span id="yfs_l84_%s">(.+?)<\/span>' % name1
    
    pattern0 = re.compile(regex0)
    pattern1 = re.compile(regex1)
    
    price0 = re.findall(pattern0, htmltext0)
    price1 = re.findall(pattern1, htmltext1)
    
    p0 =  float(str(price0)[2:-2].replace(',', ''))
    p1 =  float(str(price1)[2:-2].replace(',', ''))
    val = abs(p0 - p1)/min(p0, p1)
    final.append((round(val*100, 5), str(name0)[:-3]))
    ##print final

for comp in companies:
    t = Thread(target = find_price, args = (comp[0], comp[1],))
    t.start()
    
while(len(final) < len(companies)):
    time.sleep(0.1)
##print final
final.sort(reverse = True)
for val in final :
    print str(val[1]) + " : " + str(val[0]) + "%"
