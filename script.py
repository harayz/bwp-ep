# pip install requests
# pip install beautifulsoup4
# pip install feedgen



import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

class RSS_Maker:
    def __init__(self):
        self.url = "https://myprocurement.treasury.gov.my/iklan/tender/?search="
        self.Links = []
        self.Titles = []

    def get_data(self, Code):
        print("Scraping from Code: ", Code)
        self.urlz = self.url + Code
        print("Fetching Page 1")
        resp = requests.get(self.urlz)
        soup = BeautifulSoup(resp.content, "html.parser")

        flag =  True
        try:
            page = soup.find("div", class_="mcs_paginator")
            page = page.find_all("a")
            if ">" in page[-1].text:
                del page[-1]
                p = page[-1].text.lstrip().rstrip()
                p = int(p)
            else:
                p = page[-1].text.lstrip().rstrip()
                p = int(p)
        except:
            flag = False

        self.Scrape(soup)
        
        if flag == True:
            for i in range(2, p+1):
                print("Fetching Page ", i)
                url = self.urlz + "&pnum=" + str(i)
                resp = requests.get(url)
                soup = BeautifulSoup(resp.content, "html.parser")
                self.Scrape(soup)

        
        print("Total Links: ", len(self.Links))
        print("Total Titles: ", len(self.Titles))


    def Scrape(self, soup):
        containers = soup.find_all("div", class_="mcs_resultRecordContainer")     
        for container in containers:
            title = container.find("h4")
            title = title.text
            self.Titles.append(title)
            url = container.find("a")
            url = url["href"]
            self.Links.append(url)

    def Code_nav(self):
        codes = ["330101", "330102", "330103", "330104", "330105"]
        for x in codes:
            self.get_data(x)

    def create_rss_feed(self, filename="rss_feed.xml"):
        fg = FeedGenerator()
        fg.title("Procurement Tenders")
        fg.link(href="https://myprocurement.treasury.gov.my/")
        fg.description("Latest procurement tenders")

        for title, link in zip(self.Titles, self.Links):
            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=link)

        fg.rss_file(filename)
        print(f"RSS feed generated: {filename}")

if __name__ == "__main__":
    rss = RSS_Maker()
    rss.Code_nav()
    rss.create_rss_feed()
    print("Processing Done")
