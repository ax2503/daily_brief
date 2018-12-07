#Program to import a list of headlines from News Sources
import requests
import re
import sys

def GoogleNews(args) :
  print("**********Google News**********")
  url = 'https://news.google.com/?hl=en-AU&gl=AU&ceid=AU:en'
  r=requests.get(url, allow_redirects = True)
  open('googlenews.html','wb').write(r.content)
  f=open('googlenews.html','r')
  try :
    text = f.read()
  except UnicodeDecodeError :
    text = ''
    print ('Problem opening Google News')
  f.close()
  match = re.findall(r'<span>([^<]+)',text)

  if not args :
    for k in match :
      print(k)
  else :
    for term in args :
      for k in match :
        if term in k :
          print(k)
  return

def NewsNow(args) :
  print('**********News Now**********')
  url = 'https://www.newsnow.co.uk/h/'
  r=requests.get(url, allow_redirects = True)
  open('newsnow.html', 'wb').write(r.content)
  f = open('newsnow.html','r')
  try :
    text = f.read()
  except UnicodeDecodeError :
    text = ''
    print('Problem opening News Now')
  f.close()
  match = re.findall(r'nofollow\">([^<]+)',text)

  if not args :
    for k in match :
      print(k)
  else :
    for term in args :
      for k in match :
        if term in k :
          print(k)
  return  


def main() :
  args = sys.argv[1:]
  GoogleNews(args)
  NewsNow(args)





if __name__ == '__main__':
  main()
