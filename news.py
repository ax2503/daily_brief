#Program to import a list of headlines from News Sources
import requests

def main() :
  url = 'https://www.newsnow.co.uk/h/'
  r=requests.get(url, allow_redirects = True)
  open('newsnow.html', 'wb').write(r.content)
  f = open('newsnow.html','r')



  f.close()


if __name__ == '__main__':
  main()
