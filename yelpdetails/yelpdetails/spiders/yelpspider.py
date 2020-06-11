# -*- coding: utf-8 -*-
import scrapy
import time
from ..items import YelpdetailsItem
# from scrapy.selector import Selector
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

class YelpspiderSpider(scrapy.Spider):
    name = 'yelpspider'

    def start_requests(self):
        index = 0
        yield SeleniumRequest(
            url="https://www.yelp.com/",
            wait_time=3,
            screenshot=True,
            callback=self.parse,
            meta={'index': index},
            dont_filter=True
        )

    def parse(self, response):

        driver=response.meta['driver']
        driver.find_element_by_xpath("//input[@id='find_desc']").clear()
        search_input1 = driver.find_element_by_xpath("//input[@id='find_desc']")
        # os.chdir("..")

        # a=os.path.join(os.path.abspath(os.curdir), "/web", "/templates", "/find.txt")
        firstinput = os.path.abspath(os.curdir)+"\web\option.txt"
        secondinput = os.path.abspath(os.curdir) + "\web\location.txt"
        thirdinput = os.path.abspath(os.curdir) + "\web\catg.txt"
        fourthinput = os.path.abspath(os.curdir) + "\web\pages.txt"

        f = open(firstinput, "r")
        find=f.read().splitlines()


        f = open(secondinput, "r")
        near=f.read().splitlines()

        f = open(thirdinput, "r")
        catg = f.read().splitlines()

        f = open(fourthinput, "r")
        numpages = f.read().splitlines()

        numpages = int(numpages[0])

        length = len(find)
        index = response.meta['index']

        print()
        print()
        print()
        print(find,near)
        print()
        print()
        print()

        if(index<length):

            search_input1.send_keys(find[index])
            # find.pop(0)
            driver.find_element_by_xpath("//input[@id='dropperText_Mast']").clear()
            search_input2 = driver.find_element_by_xpath("//input[@id='dropperText_Mast']")

            search_input2.send_keys(near[index])
            # near.pop(0)
            ind = index
            index += 1

            search_button=driver.find_element_by_xpath("//button[@id='header-search-submit']")
            search_button.click()

            time.sleep(4)
            print(driver.current_url)
            page=[]
            currpage=0
            yield SeleniumRequest(
                url=driver.current_url,
                wait_time=3,
                screenshot=True,
                callback=self.numberofpages,
                meta = {'page': page,'index': index,'find': find[ind],'near': near[ind],'catg': catg[0],'numpages': numpages,'currpage': currpage},
                dont_filter=True
            )


    def numberofpages(self,response):
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        page=response.meta['page']
        catg=response.meta['catg']
        numpages=response.meta['numpages']
        currpage = response.meta['currpage']


        # details=response_obj.xpath('//li[@class="lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"]/div[@class="lemon--div__373c0__1mboc container__373c0__3HMKB hoverable__373c0__VqkG7 margin-t3__373c0__1l90z margin-b3__373c0__q1DuY padding-t3__373c0__1gw9E padding-r3__373c0__57InZ padding-b3__373c0__342DA padding-l3__373c0__1scQ0 border--top__373c0__3gXLy border--right__373c0__1n3Iv border--bottom__373c0__3qNtD border--left__373c0__d1B7K border-color--default__373c0__3-ifU"]/div/div/div[2]/div[1]/div/div/div/div/div/div/h4/span')
        details = response_obj.xpath('//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/ul/li/div')
        for detail in details:
            # a=detail.xpath(".//a/@href").get()
            # a = detail.xpath(".//a/@href").get()
            # page.append(f"https://www.yelp.com{a}")
            try:
                a = detail.xpath(".//div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a/@href").get()
            except:
                a = None

            if(a==None):
                try:
                    a = detail.xpath(".//h3/text()").get()
                except:
                    a = None
            if(a!=None):
                page.append(f"https://www.yelp.com{a}")

        # for i in page:
        #     print(i)
        index = response.meta['index']
        find = response.meta['find']
        near = response.meta['near']

        next_page = response_obj.xpath('//a[@class ="lemon--a__373c0__IEZFH link__373c0__1G70M next-link navigation-button__373c0__23BAT link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"]/@href').get()

        print(next_page)
        if (next_page and currpage<numpages):
            currpage += 1
            yield SeleniumRequest(
                url=f"https://www.yelp.com{next_page}",
                wait_time=3,
                screenshot=True,
                callback=self.numberofpages,
                meta={'page': page,'index': index,'find': find,'near': near,'catg': catg,'numpages': numpages,'currpage': currpage},
                dont_filter=True
            )
        else:
            # page.pop(0)
            print()
            print()
            print(page)
            print()
            print()
            duplicateurl=[]
            if ('Sponsored Results' in page[0] or 'Sponsored Result' in page[0]):
                category = 'Sponsored Results'
                page.pop(0)
                a = page[0]
            elif ('All Results' in page[0] or 'All Result' in page[0]):
                category = 'All Results'
                page.pop(0)
                a = page[0]
            else:
                category = None
                a = page[0]
            yield SeleniumRequest(
                url=a,
                wait_time=3,
                screenshot=True,
                callback=self.scrapepages,
                meta={'page': page,'category': category,'index': index,'find': find,'near': near,'catg': catg,'duplicateurl': duplicateurl},
                dont_filter=True
            )


    def scrapepages(self,response):
        Yelpdetails_Item = YelpdetailsItem()
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        page = response.meta['page']

        index = response.meta['index']
        find = response.meta['find']
        near = response.meta['near']
        catg = response.meta['catg']
        duplicateurl = response.meta['duplicateurl']


        try:
            name = response_obj.xpath("//h1/text()").get()
        except:
            name = None

        try:
            webname = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[4 or 3]/div/div/div[2]/div[2]/div/div/section[1 or 2]/div/div[1]/div/div[2]/p[2]/a/text()").get()
        except:
            webname = None

        if(webname != None):
            try:
                web_link  = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[4 or 3]/div/div/div[2]/div[2]/div/div/section[1 or 2]/div/div[1]/div/div[2]/p[2]/a/@href").get()
            except:
                web_link = None

            try:
                phone = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[4 or 3]/div/div/div[2]/div[2]/div/div/section[1 or 2]/div/div[2]/div/div[2]/p[2]/text()").get()
            except:
                phone = None
            try:
                direction = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3 or 4]/div/div/div[2]/div[2]/div/div/section[1 or 2]/div/div[3]/div/div[2]/p/a/@href").get()
            except:
                direction = None
        else:
            web_link = None
            try:
                phone = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[4 or 3]/div/div/div[2]/div[2]/div/div/section[1 or 2]/div/div[2 or 1]/div/div[2]/p[2]/text()").get()
            except:
                phone = None
            try:
                direction = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3 or 4]/div/div/div[2]/div[2]/div/div/section[1 or 2]/div/div[3 or 2]/div/div[2]/p/a/@href").get()
            except:
                direction = None



        try:
            category = response.meta['category']
        except:
            category = 'All Results'
        print()
        print(name)
        print(direction)
        print(web_link)
        print(webname)
        print(phone)
        print(category)
        print()
        if(name == None):
            name="NA"

        if (web_link == None):
            web_link="NA"
        else:
            web_link=f"https://www.yelp.com{web_link}"

        if (direction == None):
            direction = "NA"
        else:
            direction=f"https://www.yelp.com{direction}"

        if (webname == None):
            webname="NA"

        if (phone == None):
            phone="NA"

        # Sponsored Results
        #         # All Results

        print()
        print()
        print()
        print()
        print(catg)
        print(category)
        print()
        print()
        print()
        print()

        duplicatename = webname+category

        if((catg == category or catg == 'both') and duplicatename not in duplicateurl):
            duplicateurl.append(duplicatename)
            
            Yelpdetails_Item['Name'] = name
            Yelpdetails_Item['website_link'] = web_link
            Yelpdetails_Item['website_name'] = webname
            Yelpdetails_Item['phone'] = phone
            Yelpdetails_Item['Direction'] = direction
            Yelpdetails_Item['category'] = category
            Yelpdetails_Item['find'] = find
            Yelpdetails_Item['near'] = near
            yield Yelpdetails_Item

        page.pop(0)
        if len(page)!=0:

            if('Sponsored Results' in page[0] or 'Sponsored Result' in page[0]):
                category = 'Sponsored Results'
                page.pop(0)
                a=page[0]
            elif('All Results' in page[0] or 'All Result' in page[0]):
                category = 'All Results'
                page.pop(0)
                a=page[0]
            else:
                a=page[0]
            # a=page[0]
            yield SeleniumRequest(
                url=a,
                wait_time=3,
                screenshot=True,
                callback=self.scrapepages,
                meta={'page': page,'category': category,'index': index,'find': find,'near': near,'catg': catg,'duplicateurl': duplicateurl},
                dont_filter=True
            )

        else:
            yield SeleniumRequest(
                url="https://www.yelp.com/",
                wait_time=3,
                screenshot=True,
                callback=self.parse,
                meta={'index': index},
                dont_filter=True
            )




