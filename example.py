#Displays delayed financial information, most of which is only of interest to me personally.
#Uses publicly available information from popular websites
#Substitution of other websites is not possible as the searches for particular numbers to 
#use in calculations is done by regular expression patterns specific to the webpages that are
#downloaded.


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

def getASX200() :
  url = 'https://www.asx.com.au/asx/statistics/indexInfo.do'
  r=requests.get(url, allow_redirects=True)
  open('ASX200.html','wb').write(r.content)
  f = open('ASX200.html','r')
  text = f.read()
  match = re.search(r'XJO[\r\n]+\s+</td>[\r\n]+\s+<td nowrap="nowrap" class="price-down">[\r\n]+\s+([0-9,\.]+)',text)
  if match :
    result = match.group(1)
  else :
    result = 0 
  return result

#Returns the title of the latest news article and indicates if it is new.
def checkNewArticle() :
  f = open('LastArticle.txt','r')
  last = f.read()
  f.close()
  url = 'https://www.ainsliebullion.com.au/News.aspx'
  r=requests.get(url,allow_redirects=True)
  open('ainslienews.html','wb').write(r.content)
  f = open('ainslienews.html')
  text = f.read()
  f.close()
  match = re.search(r'<h1><a title=\"([A-Z,a-z,0-9,\s]+)',text)
  if match :
    result = match.group(1)
    if match.group(1) != last :
      newarticle = True
      f=open('LastArticle.txt','w+')
      f.write(match.group(1))
      f.close()
    else :
      newarticle = False
  else:
    result = ''
    newarticle = False
  return [result, newarticle]

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
  silver1k = silver1Kilo()
  print ('Silver 1 Kilo = ' + str(silver1k))

  print('Difference between silver spot and purchase price for one kg of silver')
  silverdiff = int((silver1k - silver * 31.15) * 100)/100
  print ('$' + str(silverdiff)  + ' ' + str(int(silverdiff/silver1k * 10000)/100) + '%')
  print()

  article = checkNewArticle()
  print ('Latest Ainslie News Article:')
  if article[1] :
    print(article[0] + ' ******new article')
  else :
    print(article[0])

  print ()

  valuedict={}

  #Calculate value of stocks
  totalstockvalue = 0
  for k in holdingdict.keys() :
    stockprice = getStockprice(k)
    dollarvalue = ((int)(holdingdict[k] * stockprice*100))/100
    print(k + " "+ str(dollarvalue))
    valuedict[k] = dollarvalue
    totalstockvalue += dollarvalue

  totalstockvalue = int(totalstockvalue * 100)/100
  print ('Total Stock Value = '+ str(totalstockvalue))

  print("DOW = " + str(getDow()))
  print('ASX200 = '  + str(getASX200()))
  

if __name__ == '__main__':
  main()
