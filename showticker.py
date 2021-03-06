#This program takes a ticker symbol and displays all the datedata in stocks.fs for the keys that match
import sys
import pickledb



def main() :
  db = pickledb.load('stocks.fs', True)
  args = sys.argv[1:]

  if not args :
    for k in db.getall() :
      print(k[:10] + ' ' + k[10:] + ' ' + db.get(k))
  else :
      for ticker in args :
        for k in db.getall() :
          if k[10:] == ticker :
            print(k[:10] + ' ' + k[10:] + ' ' + db.get(k))
      

  db.dump()  

if __name__ == '__main__':
  main()
