# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 15:48:32 2014

@author: Jaret
"""
import datetime 
import time
import urllib
from datetime import timedelta
import smtplib
from operator import truediv
from operator import sub
import numpy as np
import re
import urllib2
import calendar
import getopt
import sys
import datetime as dt
import pandas as pd
from pandas_datareader import data, wb
import pandas_datareader.data as web


def movingaverage(values,window):
    weightings = np.repeat(1.0, window) / window
    smas = np.convolve(values, weightings)[window-1:-(window-1)]    
    return smas 

def replacenan(parm):
    for kk in range(0,len(parm)):
        if type(parm[kk]) is str: 
            parm[kk] = parm[kk].strip()
            if parm[kk] != 'NaN' and parm[kk] != 'nan':
                parm[kk] = 0
    return parm
    
def datagrab(stocklist,timeper,stockgroup):
    #####EXAMPLE. TAKE OUT ONCE FUNCTION IS COMPLETE
    #stocklist = ['KO','PEP']
    #timeper = 'Daily'
    #stockgroup = 'largecap'
    #####
    
    dateNow = datetime.datetime.now()
    todaydate = dateNow.strftime('%Y-%m-%d')
        
    pastdate = dateNow-timedelta(days=30000);
    #print pastdate
    startdate = pastdate.strftime('%Y-%m-%d')

    
    ### Moving average lengths
    short = 10
    longs = 20
    overa = 1
    undera = 1
    own = 1
    sell = 1
    for z in range (0,len(stocklist)):
        if stocklist[z]=='RUT':
            StockName = '%5ERUT'
        elif stocklist[z]=='RMZ':
            StockName = '%5ERMZ'
        elif stocklist[z]=='SPXLong':
            StockName = '%5EGSPC'
        elif stocklist[z]=='TYX':
            StockName = '%5ETYX'
        elif stocklist[z]=='TNX':
            StockName = '%5ETNX'
        elif stocklist[z]=='FTSE':
            StockName = '%5EFTSE'
        elif stocklist[z]=='RMZ':
            StockName = '%5ERMZ'
        else:
            StockName = stocklist[z]
        
        if timeper == 'Daily':
            per = '1d'
        elif timeper == 'Weekly':
            per = '1wk'
        else:
            per = '1mo'
        start_date = dt.datetime(1960, 1, 1)
        if timeper == 'Daily':    
            print stocklist[z]
            
            dat = data.DataReader(StockName, 'yahoo', start_date, dt.datetime.today())
                                    
                                 
        if timeper == 'Weekly':    
            stock_d = web.DataReader(StockName, 'yahoo', start_date, dt.datetime.today())
            
            def week_open(array_like):
                return array_like[0]
            
            def week_close(array_like):
                return array_like[-1]
            
            stock_w = stock_d.resample('W',
                                how={'Open': week_open, 
                                     'High': 'max',
                                     'Low': 'min',
                                     'Close': week_close,
                                     'Volume': 'sum'}, 
                                loffset=pd.offsets.timedelta(days=-6))

            dat = stock_w[['Open', 'High', 'Low', 'Close', 'Volume']]
            print stocklist[z]
            
        if timeper == 'Monthly':                
            stock_d = web.DataReader(StockName, 'yahoo', start_date, dt.datetime.today())
            
            def week_open(array_like):
                return array_like[0]
            
            def week_close(array_like):
                return array_like[-1]
            
            stock_w = stock_d.resample('M',
                                how={'Open': week_open, 
                                     'High': 'max',
                                     'Low': 'min',
                                     'Close': week_close,
                                     'Adj Close': week_close,
                                     'Volume': 'sum'})
            
            dat = stock_w[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
#            daily_dat = pd.read_csv(stockgroup + '/Daily/' + stocklist[z] + '.csv')  
#            dat2 = [dat,daily_dat.iloc[-1:]]
#            dat = pd.concat(dat2)
            print StockName
            
        dat.to_csv(stockgroup + '/' + timeper + '/' + stocklist[z] + '.csv', mode='w', header=True)     
            
        
#        crumble_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
#        crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
#        cookie_regex = r'Set-Cookie: (.*?); '
#        quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=' + per + '&events=history&crumb={}'
#        print quote_link
#        
#        def get_crumble_and_cookie(symbol):
#            link = crumble_link.format(symbol)
#            response = urllib2.urlopen(link)
#            match = re.search(cookie_regex, str(response.info()))
#            cookie_str = match.group(1)
#            text = response.read()
#            match = re.search(crumble_regex, text)
#            crumble_str = match.group(1)
#            return crumble_str, cookie_str
#        
#        
#        def download_quote(symbol, date_from, date_to):
#            time_stamp_from = calendar.timegm(datetime.datetime.strptime(date_from, "%Y-%m-%d").timetuple())
#            time_stamp_to = calendar.timegm(datetime.datetime.strptime(date_to, "%Y-%m-%d").timetuple())
#        
#            attempts = 0
#            while attempts < 5:
#                crumble_str, cookie_str = get_crumble_and_cookie(symbol)
#                link = quote_link.format(symbol, time_stamp_from, time_stamp_to, crumble_str)
#                #print link
#                r = urllib2.Request(link, headers={'Cookie': cookie_str})
#        
#                try:
#                    response = urllib2.urlopen(r)
#                    text = response.read()
#                    print "{} downloaded".format(symbol)
#                    return text
#                except urllib2.URLError:
#                    print "{} failed at attempt # {}".format(symbol, attempts)
#                    attempts += 1
#                    time.sleep(2*attempts)
#            return ""
#        
#
#        #print get_crumble_and_cookie('KO')
#        print StockName
#        symbol_val = StockName
#        from_val = startdate
#        to_val = todaydate
#        output_val = stockgroup + '/' + timeper + '/' + stocklist[z] + '.csv'
#        event_val = "history"
##        for opt, value in options:
##            if opt[2:] == from_arg:
##                from_val = value
##            elif opt[2:] == to_arg:
##                to_val = value
##            elif opt[2:] == symbol_arg:
##                symbol_val = value
##            elif opt[2:] == event_arg:
##                event_val = value
##            elif opt[1:] == output_arg:
##                output_val = value
#    
#        print "downloading {}".format(symbol_val)
#        text = download_quote(symbol_val, from_val, to_val)
#    
#        with open(output_val, 'wb') as f:
#            f.write(text)     
            
            
            
#            try:
# elif stocklist[z] == 'FTSE':            
#            try:
#                urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/%5EFTSE?period1=220924800&period2=' + str(int(time.time())) + '&interval=1d&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
#            except:
#                urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/%5EFTSE?period1=220924800&period2=' + str(int(time.time())) + '&interval=1d&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
#
#        else:
#            if timeper == 'Monthly':
#                try:
#                    urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/' + stocklist[z] +'%?period1=0&period2=' + str(int(time.time())) + '&interval=1mo&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
#                except:
#                    urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/' + stocklist[z] +'%?period1=0&period2=' + str(int(time.time())) + '&interval=1mo&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
#               
#            elif timeper == 'Weekly':
#                try:
#                    urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/' + stocklist[z] +'%?period1=0&period2=' + str(int(time.time())) + '&interval=1wk&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
#                except:
#                    urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/' + stocklist[z] +'%?period1=0&period2=' + str(int(time.time())) + '&interval=1wk&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
#            else:
#                try:
#                    urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/' + stocklist[z] +'%?period1=0&period2=' + str(int(time.time())) + '&interval=1d&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
#                except:
#                    try:
#                        urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/' + stocklist[z] +'%?period1=0&period2=' + str(int(time.time())) + '&interval=1d&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
#                    except:
#                        try:
#                            urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/' + stocklist[z] +'%?period1=0&period2=' + str(int(time.time())) + '&interval=1d&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
#                        except:
#                            urllib.urlretrieve('https://query1.finance.yahoo.com/v7/finance/download/' + stocklist[z] +'%?period1=0&period2=' + str(int(time.time())) + '&interval=1d&events=history&crumb=xi2/OY9HHLi','/Users/jaretrogers/Desktop/Stocks/TSP/Daily/RUT.csv')
     
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 20:14:17 2014

@author: Jaret
"""

def stocklistfun(stockgroup,timeper):
    
    if stockgroup=='mediumcap':
        if timeper=='Monthly':
            stocklist = ['NDN', 'AOS', 'AAN', 'ANF', 'ABM', 'ABVT', 'ACE', 'APKT', 'ATVI', 'ATU', 'AYI', 'ACXM'\
                'ADBE', 'ADTN', 'AAP', 'AMD', 'ASX', 'ADVS', 'ACM', 'AEG','AER', 'ARO', 'AET', 'AMG', 'A',\
                'AEM', 'AGU', 'APD', 'ARG', 'AIXG', 'AKS', 'AKAM', 'ALK', 'ALB', 'ALEX', 'ALX', 'ARE', 'ALXN', 'ALGN',\
                'Y', 'ATI', 'AGN', 'ADS', 'ATK', 'AWH', 'MDRX', 'ANR', 'ALTR', 'AWC', 'DOX', 'UHAL',\
                'ACAS', 'AEO', 'AFG', 'ANAT', 'AMSC', 'AWK', 'AGP', 'AMP', 'ABC', 'AME', 'AMKR', 'APH', 'ADI', 'AXE',\
                'ANN', 'ANSS', 'AON', 'APAGF', 'APOL', 'AIT', 'AMAT', 'ATR', 'WTR', 'ACGL', 'ACI', 'ARBA',\
                'ARMH', 'AWI', 'ARRS', 'ARW', 'ASH', 'ASIA', 'ASMI', 'ASML', 'AHL', 'AIZ', 'AGO', 'AF', 'ATHN', 'AAWW',\
                'ATW', 'AUO', 'AZK', 'ADSK', 'ALV', 'AN', 'AZO', 'AVB', 'AVY', 'AVT', 'AVP', 'AVX', 'AXS', 'BHI',\
                'BLL', 'BYI', 'BMA', 'CIB', 'BOH', 'IRE', 'BBT', 'BEAV', 'BDX', 'BBBY', 'BDC', 'BMS', 'BHE', 'BRY',\
                'BBY', 'BIG', 'BIIB', 'BMRN', 'BMR', 'BLKB', 'BOKF', 'BWA', 'BXP', 'BRC', 'BRE',\
                'BEXP', 'EAT', 'BRS', 'BKS', 'BRCM', 'BR', 'BRCD', 'BAM', 'BPO', 'BRO', 'BRKR', 'CHRW',\
                'BCR', 'CA', 'CAB', 'CVC', 'CBT','COG', 'CDNS', 'CAE', 'CPN', 'CCJ', 'CAM', 'CPB', 'CP', 'CPLA', 'COF', 'CRR',\
                'CAH', 'CECO', 'CSL', 'KMX', 'CRS', 'CRI', 'CASY', 'CSH', 'CHSI', 'CBG', 'CBS', 'CE', 'CLS', 'CEL', 'CNC',\
                'CENX', 'CERN', 'CF', 'GIB', 'CRL', 'CHKP','CHE', 'CHK', 'CBI', 'PLCE', 'CEA', 'ZNH', 'CMG',\
                'CHH', 'CHD', 'CI', 'XEC', 'CTAS', 'CRUS', 'CTXS', 'CYN', 'CLC', 'CLH', 'CNL', 'CLF', 'CME', 'CMS', 'CNA', 'CNH', 'CNO',\
                'COH', 'CCE', 'KOF', 'CCH', 'CGNX', 'CTSH', 'CSTR', 'COLM', 'CBSH', 'CYH', 'CVLT', 'CBD', 'SBS', 'ELP', 'BVN',\
                'CMP', 'CSC', 'CPWR', 'CNW', 'CXO', 'CNQR', 'CNX', 'STZ', 'CEG', 'CLR', 'CBE', 'CTB', 'CPA', 'CPRT', 'CLB', 'CPO',\
                'CXW', 'CZZ', 'CSGP', 'CVD', 'CVA', 'CVH', 'COV', 'CBRL', 'CR', 'BAP', 'CACC', 'CREE', 'CRH', 'CROX', 'CCK', 'CTCM',\
                'CTRP', 'CUB', 'CBST', 'CFR', 'CMI', 'CW', 'CYMI', 'CYT', 'DHI', 'DRI', 'DVA', 'DF', 'DEG', 'DFG', 'DAL',\
                'DNR', 'XRAY', 'DV', 'DO', 'DSX', 'DKS', 'DBD', 'DLR', 'DRIV', 'DDS', 'DFS', 'DISCA', 'DISH', 'DLB', 'DTG',\
                'DLTR', 'UFS', 'DCI', 'DOV', 'DPS', 'RDY', 'DWA', 'DRC', 'DRQ', 'DRYS', 'DST', 'DSW', 'DFT', 'EJ', 'EXP', 'EWBC', 'EMN', 'EK',\
                'ETN', 'EV', 'SATS', 'EIX', 'EW', 'EP', 'EE', 'ESLT', 'ERJ', 'EME', 'EOC', 'ICA', 'P', 'ENH',\
                'EGN', 'ENR', 'EXXI', 'ENI', 'ENS', 'ESV', 'EQT', 'EFX', 'EQIX', 'ELS', 'ERIE', 'ESS', 'ESL', 'RE', 'XCO', 'EXPE',\
                'EXPD', 'EXR', 'FDS', 'FCS', 'FDO', 'FAST', 'FRT', 'FDML', 'FIS', 'FNSR', 'FCNCA', 'FSLR', 'FMER', 'FISV',\
                'FLEX', 'FLIR', 'FLO', 'FLS', 'FLR', 'FMC', 'FTI', 'FL', 'FRX', 'FST', 'FOSL', 'FWLT', 'FMS', 'FDP', 'FRO', 'FCN',\
                'FULT', 'GBL', 'GME', 'GCI', 'GDI', 'GRMN', 'IT', 'GMT', 'GPRO', 'BGC', 'GWR', 'GNTX', 'GPC', 'GNW', 'GGB', 'GA', 'GIL',\
                'GBCI', 'GPN', 'GFI', 'GR', 'GGG', 'GTI', 'GPK', 'GMCR', 'GHL', 'GEF', 'PAC', 'ASR', 'GGAL', 'TV', 'SOLR', 'GSH',\
                'GES', 'HNZ', 'HAE', 'HBI', 'HANS', 'HOG', 'HAR', 'HRS', 'HSC', 'HIG', 'HCC', 'HMA', 'HCSG', 'HLS', 'HS', 'HTLD',\
                'HL', 'HEI', 'HP', 'HSIC', 'HLF', 'MLHR', 'HES', 'HXL', 'HRC', 'HI', 'HIT', 'HITT', 'HMSY','HNI', 'HOLX', 'HMIN', 'HXM',\
                'HRL', 'HSP', 'HSNI', 'HUBG', 'HUM', 'IAG', 'IBKC', 'ICLR', 'ICON', 'IDA', 'IEX', 'IDXX', 'BIN', 'IHS', 'ILMN', 'IMAX',\
                'INFA', 'IR', 'IM', 'IART', 'ICE', 'IDCC', 'IBOC', 'IFF', 'IGT', 'IP', 'IRF', 'ISCA', 'IPG',\
                'INTU', 'ISRG', 'IVZ', 'ISBC', 'IPGP', 'IRM', 'IEF', 'IWF', 'OEF', 'IJJ', 'ITC', 'ITT',\
                'ESI', 'JBHT', 'JCP', 'JCOM', 'JASO', 'JBL', 'JKHY', 'JACK', 'JEC', 'JHX', 'JNS', 'JAH', 'JBLU',\
                'JLL', 'JOSB', 'JNPR', 'KSU', 'KDN', 'KB', 'KBR', 'K', 'KMT', 'KMR', 'KCI', 'KGC',\
                'KEX', 'KLAC', 'KNX', 'KSS', 'KNM', 'KRO', 'KT', 'KUB', 'KYO', 'LLL', 'LH', 'LRCX', 'LFL', 'LANC', 'LSTR',\
                'LDK', 'LM', 'LPS', 'LEN', 'LII', 'LUK', 'LXK', 'LPL', 'LCAPA', 'LINTA', 'LIFE', 'LTM', 'LPNT',\
                'LNCR', 'LECO', 'LNC', 'LLTC', 'LKQX', 'L', 'LOGI', 'LFT', 'LORL', 'LSI', 'LUFK', 'LULU', 'LUX', 'MTB',\
                'MDC', 'M', 'MGLN', 'MGA', 'MKTAY', 'MAN', 'MANT', 'MKL', 'GDX', 'MMC', 'MLM', 'MRVL', 'MASI', 'MAT', 'MATW',\
                'MKC', 'MDR', 'MCK', 'MDU', 'MJN', 'MWV', 'MTL', 'MDAS', 'MRX', 'MD', 'MELI', 'MDP', 'MEOH',\
                'MTD', 'MCRS', 'MSCC', 'MR', 'MTX', 'MHK', 'MOLX', 'TAP', 'MWW', 'MRH', 'MCO', 'MORN',\
                'MSM', 'MUR', 'MYL', 'MYGN', 'NBR', 'NLC', 'NDAQ', 'NFG', 'NATI', 'NSM', 'NOV', 'NAV', 'NNI', 'NETC',\
                'NTAP', 'NTES', 'NFLX', 'NSR', 'NGD', 'NJR', 'NWL', 'NFX', 'NEU', 'NXY', 'NICE', 'GAS', 'NJ',\
                'NIHD', 'NE', 'NBL', 'NMR', 'JWN', 'NTL', 'NU', 'NTRS', 'NOC', 'NWN', 'NVLS', 'NRG','NST', 'NUS', 'NUE', 'NUVA',\
                'NVE', 'NVDA', 'NVR', 'ORLY', 'OII', 'OMX', 'OGE', 'OIS', 'ODFL', 'OLN', 'OCR', 'OMC', 'OVTI', 'ONNN', 'OB', 'OKE', 'OTEX',\
                'IX', 'ORA', 'OSK', 'OMI', 'OC', 'OI', 'PFCB', 'PCAR', 'PKG', 'PLL', 'PAAS', 'PNRA', 'PRX', 'PMTC', 'PRXL',\
                'PH', 'PRE', 'PTI', 'PCX', 'PDCO', 'PTEN', 'BTU', 'PSO', 'PEGA', 'PAG', 'PNR', 'PWRD', 'PKI', 'PRGO', 'PETM', 'PCG',\
                'PPDI', 'PVH', 'PNY', 'PXD', 'PXP', 'PLT', 'PTP', 'PLXS', 'PMCS', 'PII', 'RL', 'PLCM', 'POL', 'POOL', 'BPOP', 'PRAA', 'PWER',\
                'PPG', 'PCP', 'PCLN', 'PFG', 'PRA', 'PRGS', 'PRSP', 'PL', 'PSSI', 'IIT', 'QGEN', 'QLGC',\
                'QSII', 'PWR', 'DGX', 'QSFT', 'STR', 'KWK', 'RAX', 'RSH', 'RAH', 'RMBS', 'GOLD', 'RRC', 'RJF', 'RYN', 'RTN', 'RHT', 'ENL',\
                'RUK', 'RBC', 'RGS', 'RGA', 'RS', 'RNR', 'SOL', 'RCII', 'RSG', 'RMD', 'RFMD', 'RBA', 'RVBD', 'RLI', 'RHI', 'RKT', 'ROK',\
                'COL', 'ROC', 'ROL', 'ROP', 'ROSE', 'ROST', 'ROVI', 'RDC', 'RCL', 'RGLD', 'RES', 'RDK', 'RYAAY', 'R', 'RSP', 'SAI', 'CRM',\
                'SBH', 'SNDK', 'SAPE', 'SCHN', 'SWM', 'SNI', 'CKH', 'STX', 'SEE', 'SHLD', 'SEIC','SRE', 'SMTC',\
                'SXT', 'SCI', 'SNDA', 'SJR', 'SHW', 'SHG', 'SFL', 'SHPGY', 'SIAL', 'SBNY', 'SIG', 'SLGN', 'SLAB', 'SLW', 'SVM', 'SSD',\
                'SMS', 'SINA', 'SHI', 'SIRO', 'SKM', 'SKX', 'SWKS', 'SLG', 'SLM', 'SM', 'SNN', 'SFD', 'SQM', 'SOHU', 'SWI',\
                'SLH', 'SOA', 'SON', 'BID', 'SJI', 'SUG', 'LUV', 'SWX', 'SWN', 'RWX', 'DIA','SPR', 'SPW', 'STJ', 'SFG', 'SWK',\
                'STN', 'SPLS', 'SBUX', 'STT', 'STLD', 'SRCL', 'STE', 'SLT', 'SHOO', 'SF', 'SWC', 'STM', 'STRA', 'SYK', 'SPWRA', 'SVU', 'SUSQ',\
                'SIVB', 'SFY', 'SXCI', 'SYMC','SNPS', 'TLEO', 'TLM', 'SKT', 'TGB', 'TCL', 'TTM', 'TCB',\
                'TECD', 'TECH', 'TGP', 'TOO', 'TNE', 'TDY', 'TFX', 'TDS', 'TLAB', 'TU', 'TIN', 'TPX', 'THC', 'TEN', 'TDC', 'TER', 'TX',\
                'TXRH', 'TGH', 'TXT', 'TFSL', 'AES', 'ALL', 'BCO', 'BKE', 'CAKE', 'CB', 'CLX', 'COO', 'DNB',\
                'EL', 'GPS', 'GEO', 'GT', 'GYMB', 'HAIN', 'THG', 'HSY', 'IFN', 'SJM', 'KR', 'MHP', 'MW', 'MIDD', 'NYT', 'PGR', 'SMG',\
                'TBL', 'TKR', 'TJX', 'TTC', 'VAL', 'WRC', 'WPO', 'WU', 'TMO', 'TNB', 'TC', 'THO', 'THOR', 'TIBX', 'TDW', 'TIF', 'THI', 'TSU',\
                'TIE', 'TR', 'TMK', 'TSS', 'TW', 'TSCO', 'TRH', 'TDG', 'RIG', 'THS', 'TRMB', 'TSL', 'TRN', 'TQNT', 'TGI', 'TRW', 'TUP',\
                'TKC', 'TWTC', 'TEL', 'TYC', 'TSN', 'UGI', 'ULTA', 'UPL', 'UGP', 'UMBF', 'UA', 'UIS', 'UNT', 'UNFI', 'USM', 'UTHR', 'UTR', 'UAM',\
                'UHS', 'UNM', 'URBN', 'URS', 'LCC', 'UTIW', 'VFC', 'MTN', 'VCI', 'VHI', 'VR', 'VMI', 'VCLK', 'VIT', 'VIG', 'VGK', 'VPL',\
               'VNQ', 'VB', 'VBK', 'VBR', 'VTI', 'VAR', 'VSEA', 'WOOF', 'VECO', 'VQ', 'VTR', 'PAY', 'VRSN', 'VSAT', 'VPHM',\
                'VNO', 'WRB', 'GRA', 'GWW', 'WAB', 'WACLY', 'WDR', 'WLT', 'WCRX', 'WFSL', 'WCN', 'WAT', 'WSO', 'WPI', 'WBMD', 'WTW', 'WMK',\
                'WERN', 'WCC', 'WST', 'WABC', 'WDC', 'WLK', 'WGL', 'WHR', 'WTM', 'WLL', 'WMB', 'WSM', 'WSH', 'WEC',\
                'WMS', 'WWW', 'WF', 'INT', 'WOR', 'WPPGY', 'WXS', 'WX', 'WYN', 'WYNN', 'XRX', 'XLNX', 'YHOO', 'AUY', 'YZC', 'YGE', 'ZBRA', 'ZMH'];
        else:    
            stocklist = ['NDN', 'AOS', 'AAN', 'ANF', 'ABM', 'ABVT', 'ACE', 'APKT', 'ATVI', 'ATU', 'AYI', 'ACXM'\
                'ADBE', 'ADTN', 'AAP', 'AMD', 'ASX', 'ADVS', 'ACM', 'AEG','AER', 'ARO', 'AET', 'AMG', 'A',\
                'AEM', 'AGU', 'APD', 'ARG', 'AIXG', 'AKS', 'AKAM', 'ALK', 'ALB', 'ALEX', 'ALX', 'ARE', 'ALXN', 'ALGN',\
                'Y', 'ATI', 'AGN', 'ADS', 'ATK', 'AWH', 'MDRX', 'ANR', 'ALTR', 'AWC', 'DOX', 'UHAL',\
                'ACAS', 'AEO', 'AFG', 'ANAT', 'AMSC', 'AWK', 'AGP', 'AMP', 'ABC', 'AME', 'AMKR', 'APH', 'ADI', 'AXE',\
                'ANN', 'ANSS', 'AON', 'APAGF', 'APOL', 'AIT', 'AMAT', 'ATR', 'WTR', 'ACGL', 'ACI', 'AGII', 'ARBA',\
                'ARMH', 'AWI', 'ARRS', 'ARW', 'ASH', 'ASIA', 'ASMI', 'ASML', 'AHL', 'AIZ', 'AGO', 'AF', 'ATHN','AAWW'\
                'ATW', 'AUO', 'AZK', 'ADSK', 'ALV', 'AN', 'AZO', 'AVB', 'AVY', 'AVT', 'AVP', 'AVX', 'AXS', 'BHI',\
                'BLL', 'BYI', 'BMA', 'CIB', 'BOH', 'IRE', 'BBT', 'BEAV', 'BDX', 'BBBY', 'BDC', 'BMS', 'BHE', 'BRY',\
                'BBY', 'BIG', 'BBG', 'BIO', 'BIIB', 'BMRN', 'BMR', 'BLKB', 'BOKF', 'BWA', 'BXP', 'BRC', 'BRE',\
                'BEXP', 'EAT', 'BRS', 'BKS', 'BRCM', 'BR', 'BRCD', 'BAM', 'BPO', 'BRO', 'BRKR', 'CHRW',\
                'BCR', 'CA', 'CAB', 'CVC', 'CBT','COG', 'CDNS', 'CAE', 'CPN', 'CCJ', 'CAM', 'CPB', 'CP', 'CPLA', 'COF', 'CRR',\
                'CAH', 'CECO', 'CSL', 'KMX', 'CRS', 'CRI', 'CASY', 'CSH', 'CHSI', 'CBG', 'CBS', 'CE', 'CLS', 'CEL', 'CNC',\
                'CENX', 'CERN', 'CF', 'GIB', 'CRL', 'CHKP', 'CHE', 'CHK', 'CBI', 'PLCE', 'CEA', 'ZNH', 'CMG',\
                'CHH', 'CHD', 'CI', 'XEC', 'CTAS', 'CRUS', 'CTXS', 'CYN', 'CLC', 'CLH', 'CNL', 'CLF', 'CME', 'CMS', 'CNA', 'CNH', 'CNO',\
                'COH', 'CCE', 'KOF', 'CCH', 'CGNX', 'CTSH', 'CSTR', 'COLM', 'CBSH', 'CYH', 'CVLT', 'CBD', 'SBS', 'ELP', 'BVN',\
                'CMP', 'CSC', 'CPWR', 'CNW', 'CXO', 'CNQR', 'CNX', 'STZ', 'CEG', 'CLR', 'CBE', 'CTB', 'CPA', 'CPRT', 'CLB', 'CPO',\
                'CXW', 'CZZ', 'CSGP', 'CVD', 'CVA', 'CVH', 'COV', 'CBRL', 'CR', 'BAP', 'CACC', 'CREE', 'CRH', 'CROX', 'CCK', 'CTCM',\
                'CTRP', 'CUB', 'CBST', 'CFR', 'CMI', 'CW', 'CYMI', 'CYT', 'DHI', 'DRI', 'DVA', 'DF','DEG', 'DFG', 'DAL',\
                'DNR', 'XRAY', 'DV', 'DO', 'DSX', 'DKS', 'DBD', 'DLR', 'DRIV', 'DDS', 'DFS', 'DISCA', 'DISH', 'DLB', 'DTG',\
                'DLTR', 'UFS', 'DCI', 'DOV', 'DPS', 'RDY', 'DWA', 'DRC', 'DRQ', 'DRYS', 'DST', 'DSW', 'DFT', 'EJ', 'EXP', 'EWBC', 'EMN', 'EK',\
                'ETN', 'EV', 'SATS', 'ECL', 'EIX', 'EDMC', 'EW', 'EP', 'EE', 'ESLT', 'ERJ', 'EME', 'EOC', 'ICA', 'P', 'ENH',\
                'EGN', 'ENR', 'EXXI', 'ENI', 'ENS', 'ESV', 'EQT', 'EFX', 'EQIX', 'ELS', 'ERIE', 'ESS', 'ESL', 'RE', 'XCO', 'EXPE',\
                'EXPD', 'EXR', 'FDS', 'FCS', 'FDO', 'FAST', 'FRT', 'FDML', 'FIS', 'FNSR', 'FCNCA', 'FSLR', 'FMER', 'FISV',\
                'FLEX', 'FLIR', 'FLO', 'FLS', 'FLR', 'FMC', 'FTI', 'FL', 'FRX', 'FST', 'FOSL', 'FWLT', 'FMS', 'FDP', 'FRO', 'FCN',\
                'FULT', 'GBL', 'GME', 'GCI', 'GDI', 'GRMN', 'IT', 'GMT', 'GPRO', 'BGC', 'GWR', 'GNTX', 'GPC', 'GNW', 'GGB', 'GA', 'GIL',\
                'GBCI', 'GPN', 'GFI', 'GR', 'GGG', 'GTI', 'GPK', 'GMCR', 'GHL', 'GEF', 'PAC', 'ASR', 'GGAL', 'TV', 'SOLR', 'GSH',\
                'GES', 'HNZ', 'HAE', 'HBI', 'HANS', 'HOG', 'HAR', 'HRS', 'HSC', 'HIG', 'HCC', 'HMA', 'HCSG', 'HLS', 'HS', 'HTLD',\
                'HL', 'HEI', 'HP', 'HSIC', 'HLF', 'MLHR', 'HES', 'HXL', 'HRC', 'HI', 'HIT', 'HITT', 'HMSY', 'HNI', 'HOLX', 'HMIN', 'HXM',\
                'HRL', 'HSP', 'HSNI', 'HUBG', 'HUM', 'IAG', 'IBKC', 'ICLR', 'ICON', 'IDA', 'IEX', 'IDXX', 'BIN', 'IHS', 'ILMN', 'IMAX',\
                'INFA', 'IR', 'IM', 'IART', 'IHG', 'ICE', 'IDCC', 'IBOC', 'IFF', 'IGT', 'IP', 'IRF', 'ISCA', 'IPG',\
                'INTU', 'ISRG', 'IVZ', 'ISBC', 'IPGP', 'IRM', 'IEF', 'IWF', 'OEF', 'IJJ', 'ITC', 'ITT',\
                'ESI', 'JBHT', 'JCP', 'JCOM', 'JASO', 'JBL', 'JKHY', 'JACK', 'JEC', 'JHX', 'JNS', 'JAH', 'JBLU',\
                'JLL', 'JOSB', 'JNPR', 'KSU', 'KDN', 'KB', 'KBR', 'K', 'KMT', 'KMR', 'KCI', 'KGC',\
                'KEX', 'KLAC', 'KNX', 'KSS', 'KNM', 'KRO', 'KT', 'KUB', 'KYO', 'LLL', 'LH', 'LRCX', 'LFL', 'LANC', 'LSTR',\
                'LDK', 'LM', 'LPS', 'LEN', 'LII', 'LUK', 'LXK', 'LPL', 'LCAPA', 'LINTA', 'LIFE', 'LTM', 'LPNT',\
                'LNCR', 'LECO', 'LNC', 'LLTC', 'LKQX', 'L', 'LOGI', 'LFT', 'LORL', 'LSI', 'LUFK', 'LULU', 'LUX', 'MTB',\
                'MDC', 'M', 'MGLN', 'MGA', 'MKTAY', 'MAN', 'MANT', 'MKL', 'GDX', 'MMC', 'MLM', 'MRVL', 'MASI', 'MAT', 'MATW',\
                'MKC', 'MDR', 'MCK', 'MDU', 'MJN', 'MWV', 'MTL', 'MDAS', 'MRX', 'MD', 'MELI', 'MDP', 'MEOH',\
                'MTD', 'MCRS', 'MSCC', 'MR', 'MTX', 'MHK', 'MOLX', 'TAP', 'MWW', 'MRH', 'MCO', 'MORN',\
                'MSM', 'MUR', 'MYL', 'MYGN', 'NBR', 'NLC', 'NDAQ', 'NFG', 'NATI', 'NSM', 'NOV', 'NAV', 'NNI', 'NETC',\
                'NTAP', 'NTES', 'NFLX', 'NSR', 'NGD', 'NJR', 'NWL', 'NFX', 'NEU', 'NXY', 'NICE', 'GAS', 'NJ',\
                'NIHD', 'NE', 'NBL', 'NMR', 'JWN', 'NTL', 'NU', 'NTRS', 'NOC', 'NWN', 'NVLS', 'NRG','NST', 'NUS', 'NUE', 'NUVA',\
                'NVE', 'NVDA', 'NVR', 'ORLY', 'OII', 'OMX', 'OGE', 'OIS', 'ODFL', 'OLN', 'OCR', 'OMC', 'OVTI', 'ONNN', 'OB', 'OKE', 'OTEX',\
                'IX', 'ORA', 'OSK', 'OMI', 'OC', 'OI', 'PFCB', 'PCAR', 'PKG', 'PLL', 'PAAS', 'PNRA', 'PRX', 'PMTC', 'PRXL',\
                'PH', 'PRE', 'PTI', 'PCX', 'PDCO', 'PTEN', 'BTU', 'PSO', 'PEGA', 'PAG', 'PNR', 'PWRD', 'PKI', 'PRGO', 'PETM', 'PCG',\
                'PPDI', 'PVH', 'PNY', 'PXD', 'PXP', 'PLT', 'PTP', 'PLXS', 'PMCS', 'PII', 'RL', 'PLCM', 'POL', 'POOL', 'BPOP', 'PRAA', 'PWER',\
                'PPG', 'PCP', 'PCLN', 'PFG', 'PRA', 'PRGS', 'PRSP', 'PL', 'PSB', 'PSSI', 'IIT', 'PSA', 'QGEN', 'QLGC',\
                'QSII', 'PWR', 'DGX', 'QSFT', 'STR', 'KWK', 'RAX', 'RSH', 'RAH', 'RMBS', 'GOLD', 'RRC', 'RJF', 'RYN', 'RTN', 'RHT', 'ENL',\
                'RUK', 'RBC', 'RGS', 'RGA', 'RS', 'RNR', 'SOL', 'RCII', 'RSG', 'RMD', 'RFMD', 'RBA', 'RVBD', 'RLI', 'RHI', 'RKT', 'ROK',\
                'COL', 'ROC', 'ROL', 'ROP', 'ROSE', 'ROST', 'ROVI', 'RDC', 'RCL', 'RGLD', 'RES', 'RDK', 'RYAAY', 'R', 'RSP', 'SAI', 'CRM',\
                'SBH', 'SNDK', 'SAPE', 'SCHN', 'SWM', 'SNI', 'CKH', 'STX', 'SEE', 'SHLD', 'SEIC', 'SEM', 'SRE', 'SMTC',\
                'SXT', 'SCI', 'SNDA', 'SJR', 'SHW', 'SHG', 'SFL', 'SHPGY', 'SIAL', 'SBNY', 'SIG', 'SLGN', 'SLAB', 'SLW', 'SVM', 'SSD',\
                'SMS', 'SINA', 'SHI', 'SIRO', 'SKM', 'SKX', 'SWKS', 'SLG', 'SLM', 'SM', 'SNN', 'SFD', 'SQM', 'SOHU', 'SWI',\
                'SLH', 'SOA', 'SON', 'BID', 'SJI', 'SUG', 'LUV', 'SWX', 'SWN', 'RWX', 'DIA', 'SPB', 'SPR', 'SPW', 'STJ', 'SFG', 'SWK',\
                'STN', 'SPLS', 'SBUX', 'STT', 'STLD', 'SRCL', 'STE', 'SLT', 'SHOO', 'SF', 'SWC', 'STM', 'STRA', 'SYK', 'SPWRA', 'SVU', 'SUSQ',\
                'SIVB', 'SFY', 'SXCI', 'SYMC', 'SNPS', 'SYNT', 'SYY', 'TROW', 'TLEO', 'TLM', 'SKT', 'TGB', 'TCL', 'TTM', 'TCB',\
                'TECD', 'TECH', 'TGP', 'TOO', 'TNE', 'TDY', 'TFX', 'TDS', 'TLAB', 'TU', 'TIN', 'TPX', 'THC', 'TEN', 'TDC', 'TER', 'TX',\
                'TXRH', 'TGH', 'TXT', 'TFSL', 'AES', 'ALL', 'BCO', 'BKE', 'CAKE', 'CB', 'CLX', 'COO', 'DNB',\
                'EL', 'GPS', 'GEO', 'GT', 'GYMB', 'HAIN', 'THG', 'HSY', 'IFN', 'SJM', 'KR', 'MHP', 'MW', 'MIDD', 'NYT', 'PGR', 'SMG',\
                'TBL', 'TKR', 'TJX', 'TTC', 'VAL', 'WRC', 'WPO', 'WU', 'TMO', 'TNB', 'TC', 'THO', 'THOR', 'TIBX', 'TDW', 'TIF', 'THI', 'TSU',\
                'TIE', 'TR', 'TMK', 'TSS', 'TW', 'TSCO', 'TRH', 'TDG', 'RIG', 'THS', 'TRMB', 'TSL', 'TRN', 'TQNT', 'TGI', 'TRW', 'TUP',\
                'TKC', 'TWTC', 'TEL', 'TYC', 'TSN', 'UGI', 'ULTA', 'UPL', 'UGP', 'UMBF', 'UA', 'UIS', 'UNT', 'UNFI', 'USM', 'UTHR', 'UTR', 'UAM',\
                'UHS', 'UNM', 'URBN', 'URS', 'LCC', 'UTIW', 'VFC', 'MTN', 'VCI', 'BVF', 'VHI', 'VR', 'VMI', 'VCLK', 'VIT', 'VIG', 'VGK', 'VPL',\
                'VNQ', 'VB', 'VBK', 'VBR', 'VTI', 'VAR', 'VSEA', 'WOOF', 'VECO', 'VQ', 'VTR', 'PAY', 'VRSN', 'VSAT', 'VPHM', 'VSH', 'VPRT',\
                'VNO', 'WRB', 'GRA', 'GWW', 'WAB', 'WACLY', 'WDR', 'WLT', 'WCRX', 'WFSL', 'WCN', 'WAT', 'WSO', 'WPI', 'WBMD', 'WTW', 'WMK',\
                'WERN', 'WCC', 'WST', 'WABC', 'WDC', 'WLK', 'WGL', 'WHR', 'WTM', 'WLL', 'WMB', 'WSM', 'WSH', 'WEC',\
                'WMS', 'WWW', 'WF', 'INT', 'WOR', 'WPPGY', 'WXS', 'WX', 'WYN', 'WYNN', 'XRX', 'XLNX', 'YHOO', 'AUY', 'YZC', 'YGE', 'ZBRA', 'ZMH','SBUX'];
          
    elif stockgroup=='largecap':
        if timeper=='Monthly':
            stocklist = ['MMM', 'AFL', 'T', 'ABT', 'ANF', 'ATVI', 'AET', 'AA', 'ALTR', 'MO', 'AEO', 'AEP', 'AXP', 'AMGN', 'APA',\
                'AMAT', 'ACI', 'ADM', 'AVP', 'BBT', 'BHP', 'BP', 'BCS', 'ABX', 'BAX', 'BAC', 'BBY', 'BRCM', 'CI', 'CSX',\
                'CVS', 'CNQ', 'COF', 'CCL', 'CAT', 'CNP', 'CTL', 'CHK', 'CVX', 'CHS', 'CSCO', 'C', 'CLF', 'CMCSA', 'CMA',\
                'CAG', 'COP', 'GLW', 'CS', 'DHR', 'DE', 'DB', 'DVN', 'DUK', 'DD', 'ETN', 'ECL',\
                'LLY', 'EMR', 'XOM', 'FITB', 'FHN', 'F', 'FCX', 'GCI', 'GE', 'GIS', 'GG', 'GS', 'HRB', 'HAL', 'HIG',\
                'HL', 'HES', 'HPQ', 'HON', 'HBAN', 'ITW', 'INTC', 'IBM', 'IGT', 'IP', 'IPG','IVZ', 'JCP', 'JPM', 'JBL',\
                'JNS', 'JNJ', 'JCI', 'KEY', 'KSS', 'LEN', 'LNC', 'LOW', 'M', 'MFC', 'MRO', 'MAR', 'MCD',\
                'MDT','MRK', 'MET', 'MSFT', 'MBT', 'MON', 'MS', 'NOV',  'NWL', 'NEM', 'NE', 'NOK', 'NUE', 'OXY',\
                'ORCL', 'PCG', 'PNC', 'PTEN', 'BTU', 'PEP','PBR', 'PFE', 'PBI', 'POT', 'PFG', 'PRU','QCOM', 'RF', 'RSG',\
                'RAI', 'RIO', 'SLM', 'SVU', 'SYY', 'SWY', 'SNY', 'SLB', 'STX', 'LUV', 'STJ', 'SPLS', 'SBUX', 'STT',\
                'STLD', 'STI', 'SU', 'AMTD', 'TOT', 'TLM', 'TGT', 'TXN', 'TXT', 'ALL', 'BK', 'BA', 'KO', 'DOW', 'GPS', 'SCHW',\
                'HD', 'KR', 'PG', 'PGR', 'SO', 'TRV', 'DIS', 'TWX', 'TYC', 'TSN', 'USB', 'UPS', 'UTX', 'UNH', 'UNM', 'VALE',\
                'VLO', 'VZ', 'VOD', 'WMT', 'WAG', 'WM', 'WFC', 'WY', 'WMB','XL', 'XRX', 'XLNX', 'AUY', 'YUM', 'DECK', 'CLX', 'CL'];
            
            
        else:
            stocklist = ['MMM', 'AFL', 'T', 'ABT', 'ANF', 'ATVI', 'AET', 'AA', 'ALTR', 'MO', 'AEO', 'AEP', 'AXP', 'AMGN', 'APA',\
                'AMAT', 'ACI', 'ADM', 'AVP', 'BBT', 'BHP', 'BP', 'BCS', 'ABX', 'BAX', 'BAC', 'BBY', 'BRCM', 'CI', 'CSX',\
                'CVS', 'CNQ', 'COF', 'CCL', 'CAT', 'CNP', 'CTL', 'CHK', 'CVX', 'CHS', 'CSCO', 'C', 'CLF', 'CMCSA', 'CMA',\
                'CAG', 'COP', 'GLW', 'CS', 'DHR', 'DE', 'DB', 'DVN', 'DMND', 'DFS', 'DUK', 'DD', 'XCO','ETN', 'ECL',\
                'LLY', 'EMR', 'EXPE', 'XOM', 'FITB', 'FHN', 'F', 'FCX', 'GCI', 'GE', 'GIS', 'GG', 'GS', 'HRB', 'HAL', 'HIG',\
                'HL', 'HES', 'HPQ', 'HON', 'HBAN', 'HUN', 'ITW', 'INTC', 'IBM', 'IGT', 'IP', 'IPG','IVZ', 'JCP', 'JPM', 'JBL',\
                'JNS', 'JNJ', 'JCI', 'KEY', 'KSS', 'LEN', 'LNC', 'LOW', 'M', 'MFC', 'MRO', 'MAR', 'MCD',\
                'MDT','MRK', 'MET', 'MSFT', 'MBT', 'MON', 'MS', 'MOS', 'NOV',  'NWL', 'NEM', 'NE', 'NOK', 'NUE', 'OXY',\
                'ORCL', 'PCG', 'PNC', 'PTEN', 'BTU', 'PEP','PBR', 'PFE', 'PM', 'PBI', 'POT', 'PFG', 'PRU', 'QCOM', 'RF', 'RSG',\
                'RAI', 'RIO', 'SLM', 'SVU', 'SYY', 'SWY', 'SNY', 'SLB', 'STX', 'SLW', 'LUV', 'SE', 'STJ', 'SPLS', 'SBUX', 'STT',\
                'STLD', 'STI', 'SU', 'AMTD', 'TOT', 'TLM', 'TGT', 'TCK', 'TXN', 'TXT', 'ALL', 'BK', 'BA', 'KO', 'DOW', 'GPS', 'SCHW',\
                'HD', 'KR', 'PG', 'PGR', 'SO', 'TRV', 'DIS', 'WU', 'TWX', 'TYC', 'TSN', 'USB', 'UPS', 'UTX', 'UNH', 'UNM', 'VALE',\
                'VLO', 'VZ', 'VIAB', 'V', 'VOD', 'WMT', 'WAG', 'WM', 'WFC', 'WY', 'WMB', 'WIN', 'XL', 'XRX', 'XLNX', 'AUY', 'YUM', 'DECK', 'CLX',\
                'CL'];
            
        
    
    elif stockgroup=='dividend':    
        stocklist = ['JNJ', 'CLX', 'MO', 'VZ', 'T', 'PG', 'KO', 'PEP', 'COP', 'MCD', 'CL', 'KMB', 'WAG', 'PM', 'BDX', 'MDT', 'PFE', 'RY', 'GE', 'MO'];
    elif stockgroup=='MeganRoth':
        stocklist = ['AAPL', 'MMM', 'APD', 'ATO', 'BKH', 'CVX', 'CBSH', 'CTBI', 'ED', 'XOM', 'GPC', 'LEG', 'MGEE', 'MSA','NFG', 'NWN', 'PNY',\
            'STR', 'RPM', 'SON', 'SYY', 'VVC', 'WAG', 'PEP', 'WGL', 'MO'];
        
    elif stockgroup=='smallcap':
        stocklist = ['CH', 'ABBC', 'ACET', 'AE', 'ASGR', 'AMSWA', 'ARKR', 'ARTNA','AGYS', 'ADC', 'ATAX', 'ALOT', 'BARI', 'BBSI', 'BNCN', 'CHKE',\
            'BAMM', 'BRID', 'BMTC', 'CNBC', 'CLCT', 'JCS', 'CWCO', 'DGAS', 'DHT', 'DDE', 'BAGL', 'EBTC', 'ESCA', 'ESP', 'EVOL', 'AGM', 'FISI', 'FLXS', 'FRS',\
            'GAIA', 'GOOD', 'GHM', 'GAIN', 'GHM', 'GNI', 'HQL', 'HTCO', 'HOFT', 'IIG', 'IPSU', 'IHC'];
    elif stockgroup=='preferred':
        stocklist = ['VZ','MCD', 'CHK', 'VLO', 'GOOG', 'MOS', 'SBUX', 'GPS', 'CLX', 'TGT'];
    elif stockgroup=='indexfunds':
        stocklist = ['SPY', 'UUP','GLD','USO','TLT','DIA','IWM','XLF','EEM', 'IWM', 'EFA', 'EWZ', 'XLE', 'FXI', 'GDX', 'VWO', 'IYR', 'EWJ', 'IVV', 'FAZ',\
            'FAS', 'SSO', 'OIH', 'MDY', 'XLU', 'TBT', 'XLK', 'XLB', 'XLI', 'XLV', 'EWT', 'SMH', 'QLD', 'QID', 'XLP', 'IWF', 'EWY', 'XLY', 'VTI', 'EWA', 'XRT',\
            'XME', 'IWB', 'IWO', 'KBE', 'ILF', 'IJR', 'EWC', 'EWH', 'IWS', 'RSX', 'IVW', 'RTH', 'KRE', 'IYF', 'XHB', 'EPP', 'IYM', 'XOP', 'VEA', 'EWS', 'DBC'];
    elif stockgroup=='TSP':
        stocklist = ['SPY', 'FAS', 'AGG', 'VXF', 'UUP','TZA','TNA', 'EFA','DRN','IWM','ERX','IWB','XLE','RUT','RMZ','VXF', 'TLT', 'EEM', 'SPXL', 'TMF', 'EDC', 'VGSH', 'DZK','XLY','XLP','XLF','XLI','XLK','RUT','SPXLong','TYX','TNX','TBT', 'TVIX', 'UVXY', 'IWC'];
    elif stockgroup=='Broyles':
        stocklist = ['TVIX','UVXY'];
    elif stockgroup=='Vanguard':
        stocklist = ['VCR','VDC', 'VIG','VWO','VDE','VEA','VGK','EDV','VXF','VFH','VEU','VSS','VHT','VYM','VIS','VGT','BIV','VV','BLV','VAW','MGK','MGC','MGV',\
            'VOT','VO','VOE','VNR','VPL','VNQ','VONE','VONG','VONV','VTWO','VTWG','VTWV','VTHR','VOOG','VOOV','IVOO','IVOG','IVOV','VOX','BND','VTI','VT','VPU',\
            'VTV', 'VGSH', 'VB', 'VOO', 'VUG', 'TNA','LBND','ERX','DRN', 'TMF'];
    elif stockgroup=='Portfolio':
        stocklist = ['LINE', 'NLY'];
    elif stockgroup=='Monthly':
        stocklist = ['XOM', 'PTR', 'BHP', 'CHL', 'MSFT', 'WMT', 'HBC', 'GE', 'IBM', 'JNJ', 'PG', 'VALE', 'CVX', 'KO', 'ORCL',\
        'WFC', 'NVS', 'LFC', 'MRK', 'PEP', 'INTC', 'GSK', 'PM', 'HPQ', 'FMX', 'SI', 'COP', 'SNY',\
        'EC', 'UN', 'UL', 'CHA', 'ABT', 'MCD', 'ABV', 'SNP', 'GS', 'RY', 'BTI', 'SLB', 'AZN', 'QCOM', 'STO',\
        'UTX', 'UPS', 'OXY', 'DIS', 'TD', 'MMM', 'V', 'SAP', 'BCS', 'NVO', 'BNS', 'KFT', 'SU', 'HD', 'BBVA',\
        'CMCSA', 'MT', 'BA', 'CAT', 'TEVA', 'ABB', 'AXP', 'CVS', 'FCX', 'DD', 'UNP', 'EMR', 'CNQ',\
        'INFY', 'UNH', 'NKE', 'TGT', 'WIT', 'MDT', 'CL', 'VWO', 'ERIC', 'APA', 'MS', 'CHU', 'HON', 'TWX',\
        'CUK', 'WAG', 'DOW', 'IMO', 'BLK', 'CCL', 'MET', 'TRI', 'LOW', 'NEM', 'HAL', 'DE', 'CNI',\
        'PHG', 'IBN', 'GLW', 'APC', 'DVN', 'COST', 'BAX', 'PNC', 'SPG', 'PX', 'FDX', 'KMB', 'MON', 'PUK', 'TCK',\
        'PRU', 'BEN', 'TRV', 'AFL', 'EOG', 'MRO', 'ITW', 'SYT', 'GD', 'GIS', 'TS', 'NEE', 'MFC', 'ECA', 'NSC',\
        'YUM', 'TLK', 'JCI', 'CSX', 'ADP', 'ADM', 'ENB', 'AAPL', 'GOOG', 'PBR', 'JPM', 'CSCO', 'TM', 'BBD',\
        'AMZN', 'DCM', 'UBS', 'MTU', 'HMC', 'CAJ', 'NTT', 'AMGN', 'F', 'POT', 'EMC', 'ING', 'DTV', 'PKX',\
        'BIDU', 'VMW', 'DB', 'GG', 'EBAY', 'ACN', 'SNE', 'GILD', 'MA', 'MOS', 'CELG', 'DHR',\
        'ESRX', 'DELL', 'RIMM', 'MHS', 'RCI', 'WLP', 'MBT', 'AMT', 'SHG',\
        'PTNR', 'WWE', 'FTR', 'TEO', 'CPL', 'VOD', 'VZ', 'T', 'ELNK', 'CTL', 'TEF', 'MO', 'BGS', 'NPD','AEA',\
        'UNTD', 'BXS', 'RRD', 'NYB', 'RAI', 'TSP', 'POM', 'FE', 'MMP', 'STD', 'LO', 'VLY', 'FNB', 'PGN',\
        'DUK', 'VE', 'HE', 'RGC', 'SLF', 'LLY', 'AEE', 'VVC', 'HCP', 'POR', 'PPL', 'PRGN', 'Q', 'ED', 'SO', 'SSS',\
        'SSL', 'HRB', 'NOK', 'PCL', 'BMO', 'LEG', 'TE', 'AB', 'UVV', 'CM', 'AEP', 'HOTT', 'PM',\
        'GSK', 'DPL', 'MAC', 'ATO', 'PAYX', 'SNY', 'SE', 'CNK', 'XEL', 'LMT', 'PFE', 'CAG', 'D', 'MRK', 'VTR', 'CS','GNI',\
        'VZ','FTR','DE','AMT','ATPG','BAC','GPS','MCD','KO','MOS','JWN','TGT','DVN','RIG','SLB'];

    return stocklist

def rsifunction(C,longs):
    rsi = [0 for x in range(len(C))]
    rsiup = [0 for x in range(len(C))]
    rsidown = [0 for x in range(len(C))]
    overa = 1; undera = 1;
    change = []
    upa = [0 for x in range(14)]
    downa = [0 for x in range(14)]
    overbought=[]
    oversold = []
    for i in range(0,len(C)):
      if i < longs-1:
          rsi[i] = 0;
          rsiup[i] = 0;
          rsidown[i] = 0;
      if i == longs-1:
          for j in range(0,14):
#              if C[longs + j -13] > C[longs+j-14]:
#                  upa[j] = C[longs + j -13] - C[longs+j-14]
#                  downa[j] = 0
#              else:
#                  upa[j] = 0
#                  downa[j]= -1*(C[longs+j-13] - C[longs + j -14])
            if C[longs + j -13] > C[longs+j-14]:
                  upa[j] = C[longs + j -13] - C[longs+j-14]
                  downa[j] = 0
            else:
                  upa[j] = 0
                  downa[j]= -1*(C[longs+j-13] - C[longs + j -14])
              
          rsiup[i] = sum(upa)/len(upa)
          rsidown[i] = sum(downa)/len(downa)
          if rsidown[i] == 0:
              rsi[i] = 0
          else:
              rsi[i] = 100 - (100/ (1+ (rsiup[i] / rsidown[i])))
          
      
      if i >= longs-1:
        if C[i] > C[i-1]:
            rsiup[i] = (rsiup[i-1]*13 + (C[i]-C[i-1]))/14;
            rsidown[i] = (rsidown[i-1]*13)/14;
        else:
            rsiup[i] = (rsiup[i-1]*13)/14;
            rsidown[i] = (rsidown[i-1]*13 - (C[i]-C[i-1]))/14;
        
    
        if rsidown[i]== 0:
            rsi[i] = 100;
        elif rsiup[i] == 0:
            rsi[i] = 0;
        else:
            rsi[i] = 100 - (100/ (1+ (rsiup[i] / rsidown[i])));
        
      
    
    for k in range(0,50):
        if rsi[len(rsi)-1] > 59:
            overbought.append(1);
            overa = overa + 1
        elif rsi[len(rsi)-1] < 41:
            oversold.append(1)
            undera = undera + 1
        
    return rsi

def macdfunction(C,short,longs,verylong):
    
    movavgshort = movingaverage(C,short);
    movavglong = movingaverage(C,longs);
    
    
    ema2 = movingaverage(C,2);
    ema4 = movingaverage(C,4);
    ema10 = movingaverage(C,10);
    ema12 = movingaverage(C,12);
    ema20 = movingaverage(C,longs);
    ema26 = movingaverage(C,26);
    ema30 = movingaverage(C,30);
    ema40 = movingaverage(C,40);
    ema50 = movingaverage(C,50);
    ema100 = movingaverage(C,100);
    if len(C) > 200:
        ema200 = movingaverage(C,200);
    else:
        ema200 = movingaverage(C,len(C)-10);
    
    try:    
        ema50 = movingaverage(C,50);
    except:
        ema50 = movingaverage(C,len(C)-2);
    
    try:
        ema100 = movingaverage(C,verylong);
    except:
        verylong = len(C)-5;
        ema100 = movingaverage(C,verylong);
    
    try:    
        ema200 = movingaverage(C,200);
    except:
        ema50 = movingaverage(C,len(C)-2);
    movavgshort = [float(x) for x in movavgshort]
    movavglong = [float(x) for x in movavglong]
    
    krm = len(C) - len(movavgshort)
    for ab in range(0,krm):
        movavgshort.insert(0,0.01)
    krm = len(C) - len(movavglong)
    for ab in range(0,krm):
        movavglong.insert(0,0.01)
    macd = map(sub,movavgshort,movavglong)
    macd = replacenan(macd)    
    macdsignal = movingaverage(macd,9);
    emadiff = map(truediv,movavgshort,movavglong)
    emadiff[:] = [(x - 1)*100 for x in emadiff]
    macd = [float(x) for x in macd]
    macdsignal = [float(x) for x in macdsignal]
    krm = len(C) - len(macd)
    for ab in range(0,krm):
        macd.insert(0,0)
    krm = len(C) - len(macdsignal)
    for ab in range(0,krm):
        macdsignal.insert(0,0)
    histogram = map(sub,macd,macdsignal)
    
    ##Adjust length of moving averages
    ema2 = np.concatenate((np.ones(len(C)-len(ema2)),ema2))
    ema4 = np.concatenate((np.ones(len(C)-len(ema4)),ema4))
    ema10 = np.concatenate((np.ones(len(C)-len(ema10)),ema10))
    ema12 = np.concatenate((np.ones(len(C)-len(ema12)),ema12))
    ema20 = np.concatenate((np.ones(len(C)-len(ema20)),ema20))
    ema26 = np.concatenate((np.ones(len(C)-len(ema26)),ema26))
    ema30 = np.concatenate((np.ones(len(C)-len(ema30)),ema30))
    ema40 = np.concatenate((np.ones(len(C)-len(ema40)),ema40))
    ema50 = np.concatenate((np.ones(len(C)-len(ema50)),ema50))
    ema100 = np.concatenate((np.ones(len(C)-len(ema100)),ema100))
    ema200 = np.concatenate((np.ones(len(C)-len(ema200)),ema200))

    
    return macd,macdsignal,emadiff,histogram,ema2,ema4,ema10,ema12,ema20,ema26,ema30,ema40,ema50,ema100,ema200,movavgshort,movavglong

def buynowfunction(C, H, L, rsi,macd,lowerboundrsi,upperboundrsi,ema12,ema20,ema50,ema100,finish,start,stock,DateFile):
    ##Looks for the latest closing price and determines whether a buy or sell
    ##signal has been met.
    oldbuy = [[] for i in range(5)]; oldbuysort = [[] for i in range(5)]; oldshort = [[] for i in range(5)]; 
    oldstdbuy = [[] for i in range(5)]; 
    if rsi[len(rsi)-1] < lowerboundrsi and macd[len(macd)-1] > macd[len(macd)-2] and macd[len(macd)-2] < macd[len(macd) - 3]:
        buynum2 = stock;
        sellnum2 = 'NaN';
        #     buy = rsi(len(rsi));
        #     buy = C(len(C));
    elif rsi[len(rsi)-1] > upperboundrsi and macd[len(macd)-1] < macd[len(macd)-2] and macd[len(macd)-2] > macd[len(macd) - 3]:
        sellnum2 = stock
        buynum2 = 'NaN'
        #     shortza(sellnum,1) = rsi(len(rsi));
        #     shortza(sellnum,2) = C(len(C));
    else:
        buynum2 = 'NaN';
        sellnum2 = 'NaN';

    ##std code
    ema12 = [float(x) for x in ema12]
    krm = len(C) - len(ema12)
    for ab in range(0,krm):
        ema12.insert(0,1)
    emadiffratio = map(truediv,C,ema12)
    lowerstd = 1 - .5*np.std(emadiffratio);
    ##Code to look back at past 50 days for buy signals
    
    for i in range(0,50):
        if len(rsi) > 45:
            if rsi[len(rsi)-(51-i)-1] < lowerboundrsi and macd[len(macd) - (51-i)-1] > macd[len(macd)-(52-i)-1] and macd[len(macd)-(52-i)-1] < macd[len(macd) - (53-i)-1]:
                oldbuy[0].append(stock)
                oldbuy[1].append(DateFile[len(DateFile)- (51 - i)-1]);
                oldbuy[2].append(C[len(C)-(51-i)-1])
                oldbuy[3].append(((((C[len(C)-1])/(C[len(C)-(51-i)-1]))) - 1)*100);
                oldbuy[4].append((((max(H[len(H)-(50-i)-1:len(H)]))/(C[len(C)-(51-i)-1]))-1)*100);
                oldbuysort[0].append(stock)
                oldbuysort[1].append(DateFile[len(DateFile)- (51 - i)-1]);
                oldbuysort[2].append(C[len(C)-(51-i)-1]);
                oldbuysort[3].append((((C[len(C)-1])/(C[len(C)-(51-i)-1])) - 1)*100);
                oldbuysort[4].append((((max(H[len(H)-(50-i)-1:len(H)]))/(C[len(C)-(51-i)-1]))-1)*100);
            if rsi[len(rsi) - (51-i)-1] > upperboundrsi and macd[len(macd) - (51-i)-1] < macd[len(macd)- (52-i)-1] and macd[len(macd)- (52-i)-1] > macd[len(macd) - (53-i)-1]:
                oldshort[0].append(stock);
                oldshort[1].append(DateFile[len(DateFile)- (51 - i)-1]);
                oldshort[2].append(C[len(C)-(51-i)-1]);
                oldshort[3].append((1-(C[len(C)-1]/(C[len(C)-(51-i)-1])))*100);
                oldshort[4].append((1-((min(L[len(L)-(50-i)-1:len(L)]))/(C[len(C)-(51-i)-1])))*100);
        if emadiffratio[len(emadiffratio)-(51-i)-1]< lowerstd and C[len(C) - (51-i)-1] > C[len(C)-(52-i)-1] and  C[len(C) - (52-i)-1] < C[len(C)-(53-i)-1]:
            oldstdbuy[0].append(stock);
            oldstdbuy[1].append(DateFile[len(DateFile)- (51 - i)-1]);
            oldstdbuy[2].append(C[len(C)-(51-i)-1]);
            oldstdbuy[3].append((((C[len(C)-1])/(C[len(C)-(51-i)-1])) - 1)*100);
            oldstdbuy[4].append((((max(H[len(H)-(50-i):len(H)]))/(C[len(C)-(51-i)-1]))-1)*100);

    return buynum2,sellnum2,oldbuy, oldbuysort,oldshort,oldstdbuy

def buysellfunction(C, H, L, rsi,macd,lowerboundrsi,upperboundrsi,ema10,ema20,ema50,ema100,finish,start):
    gaincol = 1;
    #Find previous buy signals, gains out to 40 days/weeks. 
    indexlonghigh = []; indexlong = []; Own = []; indexshort = []; indexshortlow = []; Short = []; predictgain = [[] for i in range(5)]; 
    gaintrack = [];  
    highgaintrack = [];    
    for j in range(start-1,len(C) - finish-1):
      if rsi[j] < lowerboundrsi and macd[j] > macd[j-1] and macd[j-1] < macd[j-2]:
          percentgain = (max(H[j+1:j+40])/C[j] - 1) * 100
          a = (H[j+1:j+40]).index(max(H[j+1:j+40]))+1
          indexlonghigh.append(j + a)
          indexlong.append(j)
          Own.append(percentgain)
          if macd[j-1] == 0:
              macd[j-1] = 0.01;
          predictgain[0].append(macd[j] / macd[j-1])
          predictgain[1].append((ema20[j] / ema100[j] - 1)*100)
          predictgain[2].append((ema10[j] / ema20[j] - 1)*100)
          predictgain[3].append(rsi[j])
          predictgain[4].append(macd[j])
          tmplist = C[j+1:j+40]
          tmplist = [x/C[j] for x in tmplist]
          gaintrack.append(tmplist)
          tmplist = H[j+1:j+40]
          tmplist = [x/C[j] for x in tmplist]
          highgaintrack.append(tmplist)
    
      elif rsi[j] > upperboundrsi and macd[j] < macd[j-1] and macd[j-1] > macd[j-2]:
          percentgain = (C[j] / (min(L[j+1:j+40]))-1) * 100;
          b = L[j+1:j+40].index(min(L[j+1:j+40]))+1;
          Short.append(percentgain)
          indexshort.append(j+b)
          indexshortlow.append(j+b)
    
    if 'gaintrack' in locals():
        m = len(highgaintrack)
        n = len(highgaintrack[0])
        mediangaintrack = []; mingaintrack = []; maxgaintrack = []; upquartile = []; loquartile = []; 
        highmediangaintrack = []; highmingaintrack = []; highmaxgaintrack = []; highupquartile = [];
        highloquartile = []; medhighgains = []; minhighgains = []; maxhighgains = []; loquartilehighgains = [];
        
        if len(highgaintrack)<40:
            park = len(highgaintrack)
        else:
            park = 40
        for ii in range (0,park):
            mediangaintrack.append(np.median(gaintrack[:][ii]))
            mingaintrack.append(min(gaintrack[:][ii]))
            maxgaintrack.append(max(gaintrack[:][ii]))
            upquartile.append(np.percentile(gaintrack[:][ii],75))
            loquartile.append(np.percentile(gaintrack[:][ii],25))
            highmediangaintrack.append(np.median(highgaintrack[:][ii]))
            highmingaintrack.append(min(highgaintrack[:][ii]))
            highmaxgaintrack.append(max(highgaintrack[:][ii]))
            highupquartile.append(np.percentile(highgaintrack[:][ii],75)) 
            highloquartile.append(np.percentile(highgaintrack[:][ii],25)) 
            temp = []       

            for jj in range(0,m):
                if ii == 0:
                    temp.append(highgaintrack[jj][ii])
                else:
                    temp.append(max(highgaintrack[jj][0:ii]))
            medhighgains.append(np.median(temp))
            minhighgains.append(min(temp))
            maxhighgains.append(max(temp))
            loquartilehighgains.append(np.percentile(temp,25))

        mediangaintrack = [x*C[len(C)-1] for x in mediangaintrack];
        mingaintrack = [x*C[len(C)-1] for x in mingaintrack];
        maxgaintrack = [x*C[len(C)-1] for x in maxgaintrack];
        upquartile = [x*C[len(C)-1] for x in upquartile];
        loquartile = [x*C[len(C)-1] for x in loquartile];
        highmediangaintrack = [x*C[len(C)-1] for x in highmediangaintrack];
        highmingaintrack = [x*C[len(C)-1] for x in highmingaintrack];
        highmaxgaintrack = [x*C[len(C)-1] for x in highmaxgaintrack];
        highupquartile = [x*C[len(C)-1] for x in highupquartile];        
        highloquartile = [x*C[len(C)-1] for x in highloquartile];   
    
    if 'percentgain' in locals():
        a = 0
    else:
        percentgain = 0;
        gaintrack = 0;
        mediangaintrack = 0; mingaintrack = 0; maxgaintrack = 0;

    if 'predictgain' in locals():
        a = 0
    else:
        predictgain = 0
    
    if 'Own' in locals():
        a = 0
    else:
        Own = 'NaN'
    
    if 'Short' in locals():
        a = 0
    else:
        Short = 'NaN';

    if 'indexlong' in locals():
        a = 0
    else:
        indexlong = 0
    
    if 'indexshort' in locals():
        a = 0
    else:
        indexshort = 0
    
    if 'indexlonghigh' in locals():
        a = 0
    else:
        indexlonghigh = 0
        
    if 'indexshortlow' in locals():
        a = 0
    else:
        indexshortlow = 0
    
    if 'upquartile' in locals():
        a = 0
    else:
        gaintrack = 0;mediangaintrack=0;maxgaintrack=0;minhighgains = 0; maxhighgains = 0;mingaintrack=0;upquartile=0;loquartile=0;highgaintrack=0;highmediangaintrack=0;highmaxgaintrack=0;highmingaintrack=0;highupquartile=0;highloquartile=0;medhighgains = 0;loquartilehighgains = 0;

    return percentgain,predictgain,Own,Short,indexlong,indexshort,indexlonghigh,indexshortlow,gaintrack,mediangaintrack,maxgaintrack,mingaintrack,upquartile,loquartile,highgaintrack,highmediangaintrack,highmaxgaintrack,highmingaintrack,highupquartile,highloquartile,medhighgains,minhighgains,maxhighgains,loquartilehighgains

def watchlistfunction(C, H, L, rsi,macd,lowerboundrsi,upperboundrsi,stock,ema50):
    ##Looks for the latest closing price and determines whether a buy or sell
    ##signal has been met. 
    if macd[len(macd)-1] < macd[len(macd)-2] and macd[len(macd)-2] < macd[len(macd)-3] and macd[len(macd)-3] < macd[len(macd) - 4]:
        trendbuy = str(stock)
        trendsell = 'NaN'
    elif macd[len(macd)-1] > macd[len(macd)-2] and macd[len(macd)-2] > macd[len(macd)-3] and macd[len(macd)-3] > macd[len(macd) - 4]:
        trendsell = str(stock)
        trendbuy = 'NaN'
    else:
        trendbuy = 'NaN' 
        trendsell = 'NaN'
    
    
    if rsi[len(rsi)-1] < 45:
        rsibuy = str(stock)
        rsisell = 'NaN'
    elif rsi[len(rsi)-1] > 55:
        rsisell = str(stock)
        rsibuy = 'NaN'
    else:
        rsisell = 'NaN'
        rsibuy = 'NaN'
    
    if macd[len(macd)-1] > macd[len(macd)-2] and macd[len(macd)-2] < macd[len(macd)-3]:
        trendchangebuy  = str(stock)
        trendchangesell = 'NaN'
    elif macd[len(macd)-1] < macd[len(macd)-2] and macd[len(macd)-2] > macd[len(macd)-3]:
        trendchangesell = str(stock)
        trendchangebuy = 'NaN'
    else:
        trendchangebuy = 'NaN';
        trendchangesell = 'NaN';
    
    
    
    if ema50[len(ema50)-1] > ema50[len(ema50)-2] and ema50[len(ema50)-2] < ema50[len(ema50)-3]:
        ematrendchangebuy = str(stock)
        ematrendchangesell = 'NaN'
    elif ema50[len(ema50)-1] < ema50[len(ema50)-2] and ema50[len(ema50)-2] > ema50[len(ema50)-3]:
        ematrendchangesell = str(stock)
        ematrendchangebuy = 'NaN'
    else:
        ematrendchangebuy = 'NaN'
        ematrendchangesell = 'NaN'
    
    
    ema50diff = map(truediv,C[49:len(C)],ema50)
    lowstd = 1-np.std(ema50diff)
    highstd = 1+np.std(ema50diff)
    if ema50diff[len(ema50diff)-1] < lowstd:
        emapricediffbuy = str(stock)
        emapricediffsell = 'NaN'
    elif ema50diff[len(ema50diff)-1] > highstd:
        emapricediffbuy = 'NaN';
        emapricediffsell = str(stock)
    else:
        emapricediffbuy = 'NaN';
        emapricediffsell = 'NaN';
    
    stdbuypoint = []
    for kk in range(0,len(ema50diff)):
        if ema50diff[kk] < lowstd and ema50diff[kk-1] >= lowstd:
            stdbuypoint.append(kk)
    faro = []
    try:
        for i in range(0,len(stdbuypoint)):
            if stdbuypoint[i] + 20 < len(H):
                faro.append((max(H[stdbuypoint[i]:stdbuypoint[i]+20])/C[stdbuypoint[i]]-1)*100)
            else:
                faro.append((max(H[stdbuypoint[i]:len(H)]))/C[stdbuypoint[i]]-1*100)            
        emapricediffmedgain = np.median(faro)
    except:
        emapricediffmedgain = -999
    
    
    return trendbuy,trendsell,rsibuy,rsisell,trendchangebuy,trendchangesell,ematrendchangebuy,ematrendchangesell,emapricediffbuy,emapricediffsell,emapricediffmedgain    
    
def trendchange(tmpvar,lag):
    ###Return indices of trend changes.
    incind = []
    decind = []
    for ax in range(lag+lag,len(tmpvar)):
        if tmpvar[ax]>tmpvar[ax-lag] and tmpvar[ax-lag]<tmpvar[ax-lag-lag]:
            incind.append(ax)
        elif tmpvar[ax]<tmpvar[ax-lag] and tmpvar[ax-lag]>tmpvar[ax-lag-lag]:
            decind.append(ax)
    return incind, decind
            
def trendchangecombo(tmpvar1,tmpvar2, lag, threshold, up):
    incind = []
    if up == 'Greater':
        for ax in range(lag+lag,len(tmpvar1)):
            if tmpvar1[ax]>tmpvar1[ax-lag] and tmpvar1[ax-lag]<tmpvar1[ax-lag-lag] and tmpvar2[ax]>threshold:
                incind.append(ax)  
    elif up == 'Less':
        for ax in range(lag+lag,len(tmpvar1)):
            if tmpvar1[ax]>tmpvar1[ax-lag] and tmpvar1[ax-lag]<tmpvar1[ax-lag-lag] and tmpvar2[ax]<threshold:
                incind.append(ax)    
    return incind
        
def priceemaratio(price,ema,threshold):
    incind = []
    decind = []
    priceema = np.ones(len(price))
    ema = np.append(np.ones(len(price)-len(ema)),ema)
    for a in range(len(price)-len(ema),len(price)):
        priceema[a] = price[a]/ema[a]
        if priceema[a]>threshold and priceema[a-1]<threshold:
            incind.append(a)
        elif priceema[a]<threshold and priceema[a-1]>threshold:
            decind.append(a)
            
    return priceema, incind, decind

def yearprice(C,dates):
    moind = []; yrind = []; MonthlyDate = []; YearlyDate = []; emamo = []; closemo = []
    for xx in range(0,len(dates)):
        if xx == 0:
            mo = dates[xx][5:7]
            yr = dates[xx][0:4]
        else:
            if dates[xx][5:7] != mo:
                moind.append(xx)
                mo = dates[xx][5:7]
                MonthlyDate.append(dates[xx][5:7]+'/'+dates[xx][8:10]+'/'+dates[xx][0:4])
            if dates[xx][0:4] != yr:
                yrind.append(xx)
                yr = dates[xx][0:4]
                YearlyDate.append(dates[xx][0:4])
        YearGains = [];YearCash = [1000]
    for a in range(0,len(yrind)):
        if a == 0:
            YearGains.append(C[yrind[0]]/C[0])

            
        else:
            YearGains.append(C[yrind[a]]/C[yrind[a-1]])
    for a in range(0,len(YearGains)):
        YearCash.append(YearCash[a]*YearGains[a])
    return YearGains, YearCash
    
    