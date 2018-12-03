import re
import requests



def main():
  url = 'https://www.ainsliebullion.com.au/'
  r=requests.get(url, allow_redirects = True)
  open('ainslie.html', 'wb').write(r.content) 
   
if __name__ == '__main__':
  main()
