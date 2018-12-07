#Program to import a list of headlines from News Sources
import requests
import re

def main() :
  url = 'https://www.newsnow.co.uk/h/'
  r=requests.get(url, allow_redirects = True)
  open('newsnow.html', 'wb').write(r.content)
  f = open('newsnow.html','r')
  text = f.read()
  match = re.findall(r'nofollow\">[^<]+',text)
  for k in match :
    print(k[10:])


  f.close()


if __name__ == '__main__':
  main()
