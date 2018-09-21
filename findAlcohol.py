from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import xlsxwriter

#Scrapes the current page and collects all alcohol names and their associated prices
#Takes a soup page from beautiful soup
def getAlcoholOnPage(soup):
    #For each alcohol result their links and scrape their name and price
    for link in soup.findAll('a', attrs={'itemprop': 'url', 'href': re.compile("^/ip/")}):
        resultLink = link.get('href')
        resultPage = 'https://www.walmart.com' + resultLink
        while True:
            try:
                webpage = urlopen(resultPage)
                break
            except:
                print('Failed to open webpage.')
        soup = BeautifulSoup(webpage, 'html.parser')
        name = soup.find('h1', attrs={'class': 'prod-ProductTitle no-margin font-normal heading-a'})
        name = name.get('content')
        print(name)
        price = soup.find('span', attrs={'class': 'price-group'})
        try:
            price = price.get('aria-label')
            print(price)
        except:
            price = 'N/A'
            print('Price not available')
        #Save the results in the list
        items.append([name, price])


#Starting point on Wal-Mart's site for alcohol
quote_page = 'https://www.walmart.com/c/kp/liquors'

#Open it up and make some soup
webpage = urlopen(quote_page)
soup = BeautifulSoup(webpage, 'html.parser')

#Get the number of page results plus one to for the exclusion in range()
numOfPages = 1;
for page in soup.find('button', attrs={'class': ''}).parent.parent.find_all('button', attrs={'class': ''}):
    numOfPages+=1

#Empty list to hold alcohol and prices
items = []

#For each page scrape the results
for page in range(numOfPages):
    if(page != numOfPages):
        #Check to see if it is the first page
        if(page != 0):
            nextPage = quote_page + '?offset=' + str((40 * page))
            print(nextPage)
            webpage = urlopen(nextPage)
            soup = BeautifulSoup(webpage, 'html.parser')
        getAlcoholOnPage(soup)

#Open workbook and add sheet
workbook = xlsxwriter.Workbook('Alcohol.xlsx')
worksheet = workbook.add_worksheet()

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for item, cost in (items):
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, cost)
    row += 1

#Close the workbook to save results
workbook.close()
