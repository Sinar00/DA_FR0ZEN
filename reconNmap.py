import requests
import scrapy
from scrapy.crawler import CrawlerProcess


# Spider class is used to do web scraping.
class MapSpider(scrapy.Spider):
    name = "Map_Spider"

    def parse(self, response):
        # identify all the image tags.
        css_selector = 'img'
        # loop through all the image tags found.
        for x in response.css(css_selector):
            # get the src attribute from the image tag and extract the value.
            newsel = '@src'
            image_link = x.xpath(newsel).extract_first()
            # check if the value is a jpg image link.
            if '.jpg' in image_link or '.jpeg' in image_link:
                print("Image Link:", image_link)
                # extract the result into json file.
                yield {
                    'Image Link': image_link,
                }
            # check if there is a next page.
            page_selector = '.next a ::attr(href)'
            next_page = response.css(page_selector).extract_first()
            if next_page:
                # if there is a next page move to the next page.
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


def recon(url):
    # headers are declared to modify the user-agent
    headers = {
        'User-Agent': 'Mobile'
    }
    # requests.get issues a get request to the url, and with the headers parameter,
    # the user-agent will be modified.
    h = requests.get(url, headers=headers)
    print("==========Reconnaissance Results==========")
    # retrieves the status code of the response and print OK if the status code is 200.
    if h.status_code == 200:
        print("Status Code: OK (%d)" % h.status_code)
    else:
        print("Status Code: Failed (%d)" % h.status_code)
    # retrieves the header of the response and print the fields out line by line.
    print("Header:")
    for x in h.headers:
        print("\t ", x, ":", h.headers[x])

    # content of the response is returned for unit test
    return h.text


def map_url(url):
    # Create a crawler process to run the scrapy without typing in command line.
    # set the output to results.json as a json file and disable logging.
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'results.json',
        'LOG_ENABLED': False
    })
    # set the process to crawl using Map spider and provide the url to crawl
    process.crawl(MapSpider, start_urls=[url])
    process.start()


def main():
    url = 'https://www.w3schools.com/w3css/w3css_images.asp'
    recon(url)
    map_url(url)



