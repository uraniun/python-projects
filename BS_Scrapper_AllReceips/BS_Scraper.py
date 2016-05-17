from bs4 import BeautifulSoup
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def htmlListtoStr(htmlList):
    resultStr=""
    for i in range(len(htmlList)):
        resultStr+=htmlList[i].text+"\n"
    return resultStr

RECIPE_URL = "http://allrecipes.com/recipe/%s/detail.aspx"
minReceiptCount=6663
maxReceiptCount=300000      #selected by me from site
myCSVFile=open("output.csv","wb")
writer=csv.DictWriter(myCSVFile,["Name","Ingradients","Details"])
writer.writeheader()

for receiptCode in range(minReceiptCount,maxReceiptCount):
    try:
        req = requests.get(RECIPE_URL%receiptCode)
        print req.status_code
        if (req.status_code != 200): raise IOError

        print RECIPE_URL % receiptCode
        htmlFile = BeautifulSoup(req.text, "html.parser")
        receiptName = htmlListtoStr(htmlFile.find_all("h1", {"class": "recipe-summary__h1"}))
        receiptIngrad = htmlListtoStr(htmlFile.find_all("span", {"class": "recipe-ingred_txt added"}))
        receiptDirect = htmlListtoStr(htmlFile.find_all("span", {"class": "recipe-directions__list--item"}))
        writer.writerow({'Name': receiptName, 'Ingradients': receiptIngrad, 'Details': receiptDirect})

    except IOError:
        pass
    except:
        print "Unexpected error"
        print RECIPE_URL%receiptCode
        quit()


