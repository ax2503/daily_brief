import re
import requests

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
  pricedict = {'AB1':0,'CBA':0}

  PMprices = calcPMprices()
  gold = PMprices[0]
  silver =PMprices[1]


  print('gold oz in aud = ' + str(gold))
  print('silver oz in aud = ' + str(silver))
  stash = (int)((gold * 10 + silver * 689)*100)/100
  print('value of stash = ' + str(stash))

  stockprice = getStockprice('AB1')
  pricedict['AB1'] = stockprice
  AB1 = stockprice * 22400
  print ('Value of AB1 = ' + str(AB1))

  stockprice = getStockprice('CBA')
  pricedict['CBA'] = stockprice
  CBA = stockprice * 371
  print ('Value of CBA = ' + str(CBA))

  print (pricedict)

if __name__ == '__main__':
  main()
