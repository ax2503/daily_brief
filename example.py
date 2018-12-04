import re
import requests

def silver1Kilo():
  url = 'https://www.ainsliebullion.com.au/products/silver-bullion/1kg-ainslie-silver-bullion/tabid/85/type/2/guid/484924f6-01bb-4d72-888f-6bebbeadc935/default.aspx'
  r=requests.get(url,allow_redirects= True)
  open('silverkg.html','wb').write(r.content)
  f = open('silverkg.html','r')
  text = f.read()
  match = re.search(r'(AUD\$<span id=\"dnn_ctr518_bullionStoreUI_lblProductDisplayPrice\">)(\d+\.\d+)',text)
  if match:
    print (match.group())
    silverkg = match.group(2)
  else:
    silverkg = 0
  
  return silverkg

#Returns a stock price, given an ASX stock code
def getStockprice(code):
  url = 'https://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes=' + code
  r=requests.get(url,allow_redirects = True)
  open(code+'.html','wb').write(r.content)
  f = open(code + '.html','r')
  text = f.read()
  match = re.search(r'(<td class=\"last\">)(\d+\.\d+)',text)
  if match : 
    codeprice = float(match.group(2))
  else :
    codeprice = 0
  return codeprice


#Returns the price of Gold and Silver in australian dollars
def calcPMprices():
  url = 'https://www.ainsliebullion.com.au/'
  r=requests.get(url, allow_redirects = True)
  open('ainslie.html', 'wb').write(r.content)
  f = open('ainslie.html','r')
  text = f.read()
  match = re.search(r'(goldOZ = )(\d+\.\d+)', text)
  if match :
    goldOZ = float(match.group(2))
  else:
    goldOZ = 0

  match = re.search(r'(aud = )(\d+\.\d+)', text)
  if match :
    aud = float(match.group(2))
  else :
    aud = 0

  match = re.search(r'(silverOZ = )(\d+\.\d+)',text)
  if match :
    silverOZ = float(match.group(2))
  else :
    silverOZ = 0

  audgold = goldOZ/aud
  audgold = ((int)(audgold * 100))/100
  audsilver = silverOZ/aud
  audsilver = ((int)(audsilver * 100))/100
  return [audgold, audsilver]  



def main():
  holdingdict = {
    'AB1':22400,'BLA' : 2000, 'CBA':371,'CCL':711 + 518, 'CLH': 2817 + 7373,
    'GEM':5528 + 722, 'LVT':3300, 'MYR':731, 'TLS':3056,
    'WOW':344 + 182+ 88, 'WPL':58 + 238, 'YOW':22000, 'ZEN': 2000 }

  PMprices = calcPMprices()
  gold = PMprices[0]
  silver =PMprices[1]


  print('gold oz in aud = ' + str(gold))
  print('silver oz in aud = ' + str(silver))
  stash = (int)((gold * 10 + silver * 689)*100)/100
  print('value of stash = ' + str(stash))

  valuedict={}

  totalstockvalue = 0
  for k in holdingdict.keys() :
    stockprice = getStockprice(k)
    dollarvalue = ((int)(holdingdict[k] * stockprice*100))/100
    print(k + " "+ str(dollarvalue))
    valuedict[k] = dollarvalue
    totalstockvalue += dollarvalue

  print('Total = ' + str(totalstockvalue))

  print ('Silver 1 Kilo = ' + str(silver1Kilo()))
  
  

if __name__ == '__main__':
  main()
