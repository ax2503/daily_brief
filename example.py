import re
import requests



def main():
  url = 'https://www.ainsliebullion.com.au/'
  r=requests.get(url, allow_redirects = True)
  open('ainslie.html', 'wb').write(r.content)
  f = open('ainslie.html','r')
  text = f.read()
  match = re.search(r'goldOZ = \d+', text)
  if match : print (match.group()) 
    
if __name__ == '__main__':
  main()
