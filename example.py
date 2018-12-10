#Displays delayed financial information, most of which is only of interest to me personally.
#Uses publicly available information from popular websites
#Substitution of other websites is not possible as the searches for particular numbers to 
#use in calculations is done by regular expression patterns specific to the webpages that are
#downloaded.
#The software can be used only on the basis that I have no responsiblity for the decisions made
#with the information provided by this program.


import re
import requests
import pickledb
import datetime

import stockvalues



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


def savePrice(db,ticker, value) :
  dbkey = str(datetime.date.today()) + ticker
  db.set (dbkey , str(value))

  return



def main():
  holdingdict = {
    'AB1':22400,'BLA' : 2000, 'CBA':371,'CCL':711 + 518, 'CLH': 2817 + 7373,
    'GEM':5528 + 722, 'LVT':3300, 'MYR':731, 'TLS':3056,
    'WOW':344 + 182+ 88, 'WPL':58 + 238, 'YOW':22000, 'ZEN': 2000 }

  db = pickledb.load('stocks.fs', True)

  PMprices = stockvalues.calcPMprices()
  gold = PMprices[0]
  silver =PMprices[1]

  print('Aussie = ' + str(PMprices[2]))
  savePrice(db,'Aussie',PMprices[2])

  print('gold oz in aud = ' + str(gold))
  savePrice(db,'gold',gold)

  print('silver oz in aud = ' + str(silver))
  savePrice(db,'silver', silver)

  stash = (int)((gold * 10 + silver * 689)*100)/100
  print('value of stash = ' + str(stash))
  savePrice(db, 'stash', stash)

  silver1k = stockvalues.silver1Kilo()
  print ('Silver 1 Kilo = ' + str(silver1k))
  savePrice(db,'silver1k', silver1k )


  print('Difference between silver spot and purchase price for one kg of silver')
  silverdiff = int((silver1k - silver * 31.15) * 100)/100
  print ('$' + str(silverdiff)  + ' ' + str(int(silverdiff/silver1k * 10000)/100) + '%')
  savePrice(db, 'silverdiff', silverdiff)
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
    stockprice = stockvalues.getStockprice(k)
    dollarvalue = ((int)(holdingdict[k] * stockprice*100))/100
    print(k + " "+ str(dollarvalue))
    valuedict[k] = dollarvalue
    savePrice(db, k, valuedict[k])
    totalstockvalue += dollarvalue

  totalstockvalue = int(totalstockvalue * 100)/100
  print ('Total Stock Value = '+ str(totalstockvalue))
  savePrice(db, 'totalstockvalue',totalstockvalue)

  DOW = stockvalues.getDow()
  print("DOW = " + str(DOW))
  savePrice(db,'DOW',DOW)
  ASX200 = stockvalues.getASX200()
  print('ASX200 = '  + str(ASX200))
  savePrice(db, 'ASX200', ASX200)
  
  db.dump()

  #Watchlist
  f = open('watchlist.txt','r')
  lines = f.readlines()
  for li in lines :
    w = li.split()
    price = stockvalues.getStockprice(w[0])
    if w[1] == 'greaterthan' and price > float(w[2]) :
      print (w[0] + ' is greater than ' + w[2])
    if w[1] == 'lessthan' and price < float(w[2]) :
      print (w[0] + ' is less than ' + w[2])
  f.close()


  

if __name__ == '__main__':
  main()
