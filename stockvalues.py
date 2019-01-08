
import re
import requests

#Returns the value of the Dow Jones Index
def getDow() :
  url = 'https://markets.businessinsider.com/index/dow_jones'
  r=requests.get(url, allow_redirects=True)
  open('dow.html','wb').write(r.content)
  f = open('dow.html','r')
  text = f.read()
  
  match = re.search(r'maximumFractionDigits:2\" data-animation=\"\" data-jsvalue=\"\d+\.\d+\">([0-9,\.]+)<',text)
  if match : 
    result = match.group(1)
  else :
    result = 0

  return result

#Returns the price of Gold and Silver in australian dollars
def calcPMprices():
  url = 'https://www.ainsliebullion.com.au/'
  r=requests.get(url, allow_redirects = True)
  open('ainslie.html', 'wb').write(r.content)
  with open('ainslie.html','r') as f :
    text = ''
    while True :
      try:
        c = f.read(1)
        if not c :
          break
        text += c
      except UnicodeDecodeError:
        print ()
  match = re.search(r'(goldOZ = )(\d+\.*\d*)', text)
  if match :
    goldOZ = float(match.group(2))
  else:
    goldOZ = 0

  match = re.search(r'(aud = )(\d+\.\d+)', text)
  if match :
    aud = float(match.group(2))
  else :
    aud = 0

  match = re.search(r'(silverOZ = )(\d+\.*\d*)',text)
  if match :
    silverOZ = float(match.group(2))
  else :
    silverOZ = 0

  audgold = goldOZ/aud
  audgold = ((int)(audgold * 100))/100
  audsilver = silverOZ/aud
  audsilver = ((int)(audsilver * 100))/100
  return [audgold, audsilver,aud]


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

#Returns the purchase price of a one kilo silver block
def silver1Kilo():
  url = 'https://www.ainsliebullion.com.au/products/silver-bullion/1kg-ainslie-silver-bullion/tabid/85/type/2/guid/484924f6-01bb-4d72-888f-6bebbeadc935/default.aspx'
  r=requests.get(url,allow_redirects= True)
  open('silverkg.html','wb').write(r.content)
  f = open('silverkg.html','r')
  text = f.read()
  match = re.search(r'(AUD\$<span id=\"dnn_ctr518_bullionStoreUI_lblProductDisplayPrice\">)(\d+\.\d+)',text)
  if match:
    silverkg = match.group(2)
  else:
    silverkg = 0
  
  return float(silverkg)

#Returns the value of the ASX200
def getASX200() :
  url = 'https://www.asx.com.au/asx/statistics/indexInfo.do'
  r=requests.get(url, allow_redirects=True)
  open('ASX200.html','wb').write(r.content)
  f = open('ASX200.html','r')
  text = f.read()
  match = re.search(r'XJO[\r\n]+\s+</td>[\r\n]+\s+<td nowrap=\"nowrap\" class=\"price-[a-z,A-Z]+\">[\r\n]+\s+([0-9,\.]+)',text)
  if match :
    result = match.group(1)
  else :
    result = 0 
  return result