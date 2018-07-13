"""
This version saves all the data scraped into a CSV file first before
Sending it back to the CSV.
"""
import scrapy
import csv
import json
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess

##----------------------------------------------------------------------
def retreiveAppData(csvfile = "auditfile.csv"): 
    """
    Retrieves App names and urls from audit data csv file.
    Returns two string lists: appname and the corresponding urls
    """
    with open(csvfile, encoding="utf8") as auditFile:
        readCSV = csv.reader(auditFile, delimiter = ',')
        urls = []
        appNames = []

        auditFile.readline() #Skips firstline
        
        for row in readCSV:
            url = row[3]
            urls.append(url)

    return urls

##----------------------------------------------------------------------
def scrapAppData(jsonfile = "result4.json"):
    """
    Retrieves scrapped data from json file and stores it in a list
    """
    json_data_file = open(jsonfile, encoding = 'utf8')
    json_data = json_data_file.read()

    listAllAppsData = []
    
    for i in range(len(json.loads(json_data))):
        data = json.loads(json_data)[i]

        category = data['category']
        description = data['description']
        last_update = data['last_update']
        installs = data['installs']
        num_ratings = data['num_ratings'].replace(',','')
        ratings = data['rating']
        price = data['price']

        if price != "Free":
            price = data['price'].replace(',','').replace('R','')

        listAppData = [description, price, ratings, num_ratings, category,
                       last_update, installs]   
        listAllAppsData.append(listAppData)

    json_data_file.close()
    
    return listAllAppsData

##------------------------------------------------------------------------
def placeAppData(listData, csvfile = "auditfileOut4.csv"):
    """
    Places Description, Price, Relevance, Rating, Number of ratings, Category,
    Last update and Installs data into the csv file.
    """
    with open(csvfile, "w", encoding="utf8", newline='') as out_file:
        rowWriter = csv.writer(out_file, delimiter=',')
        
        row = ['App Name','Description','Price','Google Play URL',
               'App developer','Google Play developer URL', 'Relevance',
               'Rating', 'Number of ratings', 'Category', 'Country',
               'Last updated', 'Installs']
        
        rowWriter.writerow(row)

        row = ['']*13
        
        for app in range(len(listData)):
            row[1] = listData[app][0] #description
            row[2] = listData[app][1] #price
            row[7] = listData[app][2] #rating
            row[8] = listData[app][3] #numRatings
            row[9] = listData[app][4] #category
            row[11] = listData[app][5] #lastUpdate
            row[12] = listData[app][6] #installs
            #row[8] = listData[app][0] #relevance

            rowWriter.writerow(row)
  

##--------------------------------------------------------------------------
class MTNappsSpider(scrapy.Spider):
    name = "MTNappsSpider"
    allowed_domains = ["https://play.google.com"]
    start_urls = retreiveAppData()

    ##To Find country use website link.
    ##Coming up in version 2

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_data, dont_filter=True)

    ##https://stackoverflow.com/questions/31735436/
    ##scrapy-only-scrapes-the-first-start-url-in-a-list-of-15-start-urls

    def parse_data(self, response):
        #Gets rid of 'Buy ' at the end of the price if the app is not free.
        if response.css('.play-button span::text').extract()[8] == 'Install':
            price = 'Free'
        else:
            price = response.css('.play-button span::text').extract()[8][:-4]
            
        description = response.css('.text-body div::text').extract()[0]

        try:
            rating = response.css('.score::text').extract()[0]
        except IndexError:
            rating = ""

        try:
            num_ratings = response.css('.reviews-num::text').extract()[0]
        except IndexError:
            num_ratings = ""
          
        yield {
            'description' : description,
            'price' : price,     
            'rating' : rating,
            'num_ratings' : num_ratings,
            'app_name' : response.css('.id-app-title::text').extract()[0],
            'app_developer' : response.css('.primary span::text').extract()[0],
            #'developer_url' : response.css('.document-subtitle primary::attr(href)').extract()[0],  ##Not working
            'category' : response.css('.category span::text').extract()[0],
            'last_update' : response.css('.meta-info:nth-child(1) .content::text').extract()[0],
            'installs' : response.css('.meta-info:nth-child(2) .content::text').extract()[0],
            #'country' : country,
            #'developer'
        }
    
##--------------------------------------------------------------------------
def main():
    urls = retreiveAppData()
    process = CrawlerProcess(
        {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
         'FEED_FORMAT': 'json', 'FEED_URI': 'result.json'})
    process.crawl(MTNappsSpider)
    process.start()
    
    data = scrapAppData()

    placeAppData(data)
        

if __name__ == "__main__":
    main()
