# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 19:58:38 2015

@author: jaretrogers

This is a script to analyze a single stock.
"""

from pylab import * 
import numpy as np
from operator import truediv
from operator import sub
from operator import add
from scipy.signal import argrelextrema
import operator
import pandas as pd
import datagrabfunction

def indices(a, func):
    return [kk for (kk, val) in enumerate(a) if func(val)]
    
def lagcalc(arrint, lag):
    tmparr = np.ones(len(arrint))
    tmppctarr = np.ones(len(arrint))
    for az in range(0,len(arrint)-lag):
        tmparr[az] = arrint[az+lag]
        tmppctarr[az] = arrint[az+lag]/arrint[az]
    tmparr[len(arrint)-lag:len(arrint)]=tmparr[len(arrint)-lag-1]
    tmppctarr[len(arrint)-lag:len(arrint)]=tmppctarr[len(arrint)-lag-1]
    return tmparr, tmppctarr
    

StockList = 'TVIX'

tmpfile = '/Users/jaretrogers/Desktop/Stocks/TSP/Daily/'+ StockList + '.csv'
fid = open(tmpfile,'r')
d = np.loadtxt(fid,
   delimiter = ',',
   dtype = {'names': ('col1','col2','col3','col4','col5','col6','col7'),
             'formats': ('S10','S10','S10','S10','S10','S10','S10')})
fid.close()  

tmpdate = [column[0] for column in d];
del(tmpdate[0]);
DateRead = np.flipud(tmpdate) 

tmpop = [column[1] for column in d];
del(tmpop[0]);
tmpop = [float(i) for i in tmpop]
Open = np.flipud(tmpop) 

tmphi = [column[2] for column in d];
del(tmphi[0]);
tmphi = [float(i) for i in tmphi]
High = np.flipud(tmphi)

tmplo = [column[3] for column in d];
del(tmplo[0]);
tmplo = [float(i) for i in tmplo]
Low = np.flipud(tmplo)

tmpcl = [column[6] for column in d];
del(tmpcl[0]);
tmpcl = [float(i) for i in tmpcl]
CloseAdj = np.flipud(tmpcl) 

tmpcl = [column[4] for column in d];
del(tmpcl[0]);
tmpcl = [float(i) for i in tmpcl]
Close = np.flipud(tmpcl) 

tmpvol = [column[5] for column in d];
del(tmpvol[0]);
tmpvol = [float(i) for i in tmpvol]
Volume = np.flipud(tmpvol) 

rsi = datagrabfunction.rsifunction(CloseAdj,14)
macd,macdsignal,emadiff,histogram,ema2,ema4,ema10,ema12,ema20,ema26,ema30,ema40,ema50,ema100,ema200,movavgshort,movavglong = datagrabfunction.macdfunction(CloseAdj,10,20,100)
YearGain, YearCash = datagrabfunction.yearprice(CloseAdj,DateRead)
###Look at Close price at specified number of days in future
CloseLag1, CloseLagPct1 = lagcalc(CloseAdj,1)
CloseLag10, CloseLagPct10 = lagcalc(CloseAdj,10)
CloseLag30, CloseLagPct30 = lagcalc(CloseAdj,30)
CloseLag60, CloseLagPct60 = lagcalc(CloseAdj,60)
CloseLag90, CloseLagPct90 = lagcalc(CloseAdj,90)
CloseLag180, CloseLagPct180 = lagcalc(CloseAdj,180)
CloseLag360, CloseLagPct360 = lagcalc(CloseAdj,360)

##FIND RSI VALUES LESS THAN XX
inds1 = indices(rsi,lambda x: x<25)
gg = [CloseLagPct30[i] for i in inds1]
ss = [DateRead[i] for i in inds1]

##Trend changes in EMA, MACD
MACDinc, MACDdec = datagrabfunction.trendchange(macd,1)
EMA50inc, EMA50dec = datagrabfunction.trendchange(ema50,1)

##Custom combo changes
MACDRSIcombo = datagrabfunction.trendchangecombo(macd,rsi,1,30,'Less')

##Price/EMA ratio
PriceEMA100ratio,PriceEMA100inc, PriceEMA100dec = datagrabfunction.priceemaratio(CloseAdj,ema100,1.1)

gg = CloseLagPct90[EMA50inc]

twoemaratio = np.ones(len(ema12))
for i in range(0,len(PriceEMA100ratio)):
    if PriceEMA100ratio[i] > 2:
        PriceEMA100ratio[i] = 1
    twoemaratio[i] = ema12[i]/ema100[i]
    if twoemaratio[i] >2:
        twoemaratio[i] = 1
    
#######TEST SECTIONS

#tmpbuy = [201]; tmpsell = []; tmpgain = []; tmpcash = [1000]; az = 201
#kr = 1;
#for az in range(201,len(ema200)):
#    if ((ema100[az]<ema100[az-1] and twoemaratio[az]>twoemaratio[az-1] and twoemaratio[az-1]<twoemaratio[az-2]) or (ema100[az]>ema100[az-1] and ema100[az-1]<ema100[az-2])) and kr == 0:
#        tmpbuy.append(az)
#        kr = 1;  
#    elif ((ema100[az]<ema100[az-1] and ema100[az-1]>ema100[az-2]) or (ema100[az]<ema100[az-1] and ema100[az-1]<ema100[az-2] and twoemaratio[az]<twoemaratio[az-1] and twoemaratio[az-1]>twoemaratio[az-2])) and kr == 1:
#        tmpsell.append(az)
#        kr = 0;
#    az +=1
#    
#for azz in range(0,len(tmpsell)):
#    tmpgain.append(CloseAdj[tmpsell[azz]]/CloseAdj[tmpbuy[azz]])
#    tmpcash.append(tmpcash[len(tmpcash)-1]*tmpgain[len(tmpgain)-1])
#    
#plt.figure(1)
#plt.plot(CloseAdj[0:1000])
#plt.plot(ema100[0:1000],'r')
#plt.plot(tmpbuy[0:8],ema100[tmpbuy[0:8]],'.',markersize=5)
#plt.plot(tmpsell[0:8],ema100[tmpsell[0:8]],'.k',markersize=5)
    
#############
#kr = 0;tmpbuy = []; tmpsell = []; tmpgain = []; tmpcash = [1000]; 
#for az in range(0,len(ema200)):
#    if ((CloseAdj[az]>ema200[az]*.9 and macd[az]>macd[az-1] and macd[az-1]<macd[az-2]) and rsi[az]<40 and kr == 0):
#            tmpbuy.append(az)
#            kr = 1;  
#    if ((rsi[az]<50 and rsi[az-1]>50) or (CloseAdj[az]<ema200[az]*.9)) and kr == 1:
#        tmpsell.append(az)
#        kr = 0;
#for azz in range(0,len(tmpsell)):
#    tmpgain.append(CloseAdj[tmpsell[azz]]/CloseAdj[tmpbuy[azz]])
#    tmpcash.append(tmpcash[len(tmpcash)-1]*tmpgain[len(tmpgain)-1])   
#
#plt.figure(1)
#plt.plot(CloseAdj)
#plt.plot(ema200,'r')
#plt.plot(tmpbuy,CloseAdj[tmpbuy],'.k',markersize=8)
#plt.plot(tmpsell,CloseAdj[tmpsell],'.r',markersize=8)    
#plt.savefig('STOCKS.png', format='png', dpi=100)    
#print 'Median gain is: '+ str(median(tmpgain))
#print 'Mean gain is: '+ str(mean(tmpgain))
#print 'Cash is: ' + str(tmpcash[len(tmpcash)-1])
#
#while az<len(ema200):
#    while az<len(ema200) and ema100[az]>ema100[az-1]:
#        az = az+1
#    tmpsell.append(az)
#    while az<len(ema200) and ema100[az]<ema100[az-1]:
#        if twoemaratio[az]>twoemaratio[az-1] and twoemaratio[az-1]<twoemaratio[az-2]:
#            tmpbuy.append(az)
#            while az<len(ema200) and twoemaratio[az]>twoemaratio[az-1] :
#                az = az+1
#            tmpsell.append(az)
#        az = az+1
#
#    az = az+1


#Maxes = argrelextrema(CloseAdj, np.greater,order=50)
#Mins = argrelextrema(CloseAdj, np.less,order=50)
#Maxes = Maxes[0]; Mins = Mins[0]
#
#RsiMax = [rsi[i] for i in Maxes];
#ema200Max = [PriceEMA100ratio[i] for i in Maxes]
#if RsiMax[0]== 0:
#    del(RsiMax[0])
#RsiMin = [rsi[i] for i in Mins];
#ema200Min = [PriceEMA100ratio[i] for i in Mins]
#if RsiMin[0]== 0:
#    del(RsiMin[0])
##For values .... x[argrelextrema(x, np.greater)[0]]
#print mean(gg)
#
##tmpbuy = []; tmpgain = []; tmpcash = [1000]; az = 201
##while az<len(ema200):
##    if CloseAdj[az]>ema200[az] and CloseAdj[az-1]<ema200[az-1]:
##        tmpbuy.append(az)
##        while CloseAdj[az]>ema200[az] and az<len(ema200)-1:
##            az = az+1
##        tmpgain.append(CloseAdj[az]/CloseAdj[tmpbuy[len(tmpbuy)-1]])
##    else:
##        az = az+1
#
##emaratio = []
##for azz in range(0,len(CloseAdj)):
##    emaratio.append(ema50[azz]/ema200[azz])
##    if azz <=200:
##        emaratio[azz] = 1
##emaratio = np.array(emaratio)
#emarecentchange = np.ones(len(ema50))
#for ax in range(10,len(emarecentchange)):
#    emarecentchange[ax] = ema50[ax]/ema50[ax-10]
#    if emarecentchange[ax]>2:
#        emarecentchange[ax] = 1
#
##plot(emaratio[200:len(emaratio)])
##plt.figure(figsize=(18,9))
##plt.plot(CloseAdj)
##plt.plot(tmpbuy,CloseAdj[tmpbuy],'.',markersize=15)
##plt.plot(ema200)
###plt.plot(CloseAdj[50:Maxes[89]])
###plt.plot(Maxes[50:89],CloseAdj[Maxes[50:89]],'.',markersize=10)
###plt.plot(ema200[50:Maxes[89]])
##plt.plot()
#
###test code for above EMA200
#
####simulate trading with emaratio
##ax = 2; own=0; notown=0;
##buy = []; sell = []
##buyprice = .99;
##sellprice = 1.01;
##while ax < len(emaratio):
##    if emaratio[ax]< buyprice and own==0 and ax <= len(emaratio) and emaratio[ax]>emaratio[ax-1] and emaratio[ax-1]<emaratio[ax-2]:
##        own = 1; buy.append(ax); notown = 0;
##    elif emaratio[ax]>sellprice and notown == 0 and own==1 and ax <= len(emaratio) and emaratio[ax]<emaratio[ax-1] and emaratio[ax-1]>emaratio[ax-2]:
##        notown = 1; sell.append(ax); own = 0;
##    else:
##        ax +=1
##
##
##BuyPrice = []; SellPrice = []; Gains = []; CashStart = [1000]
##for i in range(0,len(sell)):
##    BuyPrice.append(CloseAdj[buy[i]])
##    SellPrice.append((CloseAdj[sell[i]]))
##    Gains.append((CloseAdj[sell[i]])/((CloseAdj[buy[i]])))
##    CashStart.append(Gains[len(Gains)-1]*CashStart[len(CashStart)-1])
#
#
##plot(emaratio[200:len(emaratio)])
##plt.figure(figsize=(8,4))
##plt.plot(emaratio)
##plt.plot(buy,emaratio[buy],'.',markersize=15)
##plt.plot(sell,emaratio[sell],'.',markersize=15)
#
#
##plt.plot(CloseAdj)
##plt.plot(tmpbuy,CloseAdj[tmpbuy],'.',markersize=15)
##plt.plot(ema200)
###plt.plot(CloseAdj[50:Maxes[89]])
###plt.plot(Maxes[50:89],CloseAdj[Maxes[50:89]],'.',markersize=10)
###plt.plot(ema200[50:Maxes[89]])
##plt.plot()    
#
#emasideways = np.zeros(len(emarecentchange))
#emaup = np.zeros(len(emarecentchange))
#emadown = np.zeros(len(emarecentchange))
#
#for i in range(0,len(emarecentchange)):
#    if emarecentchange[i]>1.005:        
#        emaup[i] = 1
#    elif emarecentchange[i]<=1.005 and emarecentchange[i]>=.995:
#        emasideways[i] = 1
#    else:
#        emadown[i] = 1
#        
#ax = 2; own=0; notown=0; shortown = 0; shortnotown = 0;i = 2;
#buy = []; sell = [];
#short =[]; cover = [];
#
##Test MACD code with various ema trends
#while i < len(CloseAdj):
#    if emasideways[i] == 1 and macd[i]>macd[i-1] and macd[i-1]<macd[i-2] and rsi[i]<40 and i <= len(CloseAdj) and own == 0:
#        buy.append(i); own = 1; i+=1;
#    elif macd[i]<macd[i-1] and own == 1 and i <= len(CloseAdj):
#        sell.append(i); own = 0; i+=1;
#    else:
#        i +=1
#        
#
##buyprice = 1.007;
##sellprice = 1;
##while ax < len(emarecentchange):
##    if emarecentchange[ax-1]< buyprice and emarecentchange[ax] > buyprice and own==0 and ax <= len(emarecentchange):
##        own = 1; buy.append(ax); notown = 0; ax +=1;
##    elif emarecentchange[ax-1]> buyprice and emarecentchange[ax] < buyprice and own==1 and ax <= len(emarecentchange):
##        notown = 1; sell.append(ax); own = 0; ax +=1;
##    elif emarecentchange[ax-1]> sellprice and emarecentchange[ax] <= sellprice and shortown==0 and ax <= len(emarecentchange):
##        shortown = 1; short.append(ax); ax+=1;
##    elif emarecentchange[ax-1]< sellprice and emarecentchange[ax] >= sellprice and shortown==1 and ax <= len(emarecentchange):
##        shortown = 0; cover.append(ax); ax+=1;       
##    else:
##        ax +=1       
##        
#BuyPrice = []; SellPrice = []; Gains = []; CashStart = [1000]; ShortGains = []
#for i in range(0,len(sell)):
#    BuyPrice.append(CloseAdj[buy[i]])
#    SellPrice.append((CloseAdj[sell[i]]))
#    Gains.append((CloseAdj[sell[i]])/((CloseAdj[buy[i]])))
#    CashStart.append(Gains[len(Gains)-1]*CashStart[len(CashStart)-1]) 
##for i in range(0,len(cover)):
##    ShortGains.append((CloseAdj[short[i]])/((CloseAdj[cover[i]])))       
#        
##plt.figure(figsize=(18,9))
#plt.figure(1)        
#plt.plot(CloseAdj)
##plt.plot(ema200,'r')
#plt.bar(range(len(emadown)),CloseAdj*emaup)
#plt.plot(buy,CloseAdj[buy],'.k',markersize=15)
#plt.plot(sell,CloseAdj[sell],'.',markersize=15)   
#plt.savefig('StockTest.png', format='png', dpi=100)     
#        
#print "Cash is $" + str(CashStart[len(CashStart)-1])
#for an in range(0,len(tmpgain)):
#    tmpcash.append(tmpcash[len(tmpcash)-1]*tmpgain[an])


###TVIX TEST
HL = []
for a in range(0,len(High)):
    HL.append(High[a]/Low[a])

VolumeVol = np.ones(len(Volume)); CloseVol = np.ones(len(Volume)); HLVol = np.ones(len(Volume)); 
for x in range(3,len(Volume)):
    VolumeVol[x] = max(Volume[x-3:x])/min(Volume[x-3:x])
    CloseVol[x] = max(CloseAdj[x-3:x])/min(CloseAdj[x-3:x])
    HLVol[x] = max(HL[x-3:x])/min(HL[x-3:x])
    

az = 0; km = 0; tmpshort = [0]; tmpcover = []
while az<len(Volume):
    while az<len(Volume) and HLVol[az]<1.15 and km == 0:
        az = az+1
    tmpcover.append(az)
    km = 1
    while az<len(Volume) and HLVol[az]>=1.15 and km == 1:
        az = az + 1
    tmpshort.append(az)
    km = 0

if len(tmpshort)>len(tmpcover):
    tmpshort = tmpshort[0:len(tmpshort)-1]
    
ShortGains = []; CashGains = [1000]
for xx in range(0,len(tmpshort)-1):
    ShortGains.append(1 + ((CloseAdj[tmpshort[xx]]-CloseAdj[tmpcover[xx]])/CloseAdj[tmpshort[xx]]))
    CashGains.append(CashGains[len(CashGains)-1]*ShortGains[len(ShortGains)-1])