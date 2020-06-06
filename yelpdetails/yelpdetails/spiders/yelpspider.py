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
        yield SeleniumRequest(
            url="https://www.yelp.com/",
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):

        driver=response.meta['driver']
        search_input1 = driver.find_element_by_xpath("//input[@id='find_desc']")
        # os.chdir("..")

        # a=os.path.join(os.path.abspath(os.curdir), "/web", "/templates", "/find.txt")
        firstinput = os.path.abspath(os.curdir)+"\web\option.txt"
        secondinput = os.path.abspath(os.curdir) + "\web\location.txt"

        f = open(firstinput, "r")
        find=f.read()

        f = open(secondinput, "r")
        near=f.read()
        print()
        print()
        print()
        print(find,near)
        print()
        print()
        print()
        search_input1.send_keys(find)

        driver.find_element_by_xpath("//input[@id='dropperText_Mast']").clear()
        search_input2 = driver.find_element_by_xpath("//input[@id='dropperText_Mast']")

        search_input2.send_keys(near)


        search_button=driver.find_element_by_xpath("//button[@id='header-search-submit']")
        search_button.click()

        time.sleep(4)
        print(driver.current_url)
        page=[]
        yield SeleniumRequest(
            url=driver.current_url,
            wait_time=3,
            screenshot=True,
            callback=self.numberofpages,
            meta = {'page': page}
        )


    def numberofpages(self,response):
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        page=response.meta['page']
        details=response_obj.xpath('//li[@class="lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU"]/div[@class="lemon--div__373c0__1mboc container__373c0__3HMKB hoverable__373c0__VqkG7 margin-t3__373c0__1l90z margin-b3__373c0__q1DuY padding-t3__373c0__1gw9E padding-r3__373c0__57InZ padding-b3__373c0__342DA padding-l3__373c0__1scQ0 border--top__373c0__3gXLy border--right__373c0__1n3Iv border--bottom__373c0__3qNtD border--left__373c0__d1B7K border-color--default__373c0__3-ifU"]/div/div/div[2]/div[1]/div/div/div/div/div/div/h4/span')
        for detail in details:
            a=detail.xpath(".//a/@href").get()
            page.append(f"https://www.yelp.com{a}")

        # for i in page:
        #     print(i)

        next_page = response_obj.xpath('//a[@class ="lemon--a__373c0__IEZFH link__373c0__1G70M next-link navigation-button__373c0__23BAT link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"]/@href').get()

        print(next_page)
        if (next_page):
            yield SeleniumRequest(
                url=f"https://www.yelp.com{next_page}",
                wait_time=3,
                screenshot=True,
                callback=self.numberofpages,
                meta={'page': page}
            )
        else:
            yield SeleniumRequest(
                url=page[0],
                wait_time=3,
                screenshot=True,
                callback=self.scrapepages,
                meta={'page': page}
            )


    def scrapepages(self,response):
        Yelpdetails_Item = YelpdetailsItem()
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        page = response.meta['page']



        # if(response_obj.xpath("(//*[@id='wrap']/div[4/]/div/div[@class='lemon--div__373c0__1mboc margin-t3__373c0__1l90z margin-b6__373c0__2Azj6 border-color--default__373c0__3-ifU']/div/div/div[2]/div[2]/div/div/section[@class='lemon--section__373c0__fNwDM border-color--default__373c0__3-ifU']/div/div[@class='lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU']/div/div/p[@class='lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-'])[2]/text()").get()):
        #     phone=response_obj.xpath("(//*[@id='wrap']/div[4/]/div/div[@class='lemon--div__373c0__1mboc margin-t3__373c0__1l90z margin-b6__373c0__2Azj6 border-color--default__373c0__3-ifU']/div/div/div[2]/div[2]/div/div/section[@class='lemon--section__373c0__fNwDM border-color--default__373c0__3-ifU']/div/div[@class='lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU']/div/div/p[@class='lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-'])[2]/text()").get()
        # else:
        #     phone='NA'
        # try:
        #     phone = response_obj.xpath("(//*[@id='wrap']/div[4/]/div/div[@class='lemon--div__373c0__1mboc margin-t3__373c0__1l90z margin-b6__373c0__2Azj6 border-color--default__373c0__3-ifU']/div/div/div[2]/div[2]/div/div/section[@class='lemon--section__373c0__fNwDM border-color--default__373c0__3-ifU']/div/div[@class='lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU']/div/div/p[@class='lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-'])[2]/text()").get()
        # except:
        #     phone="NA"
        # try:
        #     name=response_obj.xpath("//h1/text()").get()
        # except:
        #     name = "NA"
        # try:
        #     weblink = response_obj.xpath("(//*[@id='wrap']/div[4]/div/div[@class='lemon--div__373c0__1mboc margin-t3__373c0__1l90z margin-b6__373c0__2Azj6 border-color--default__373c0__3-ifU']/div/div/div[2]/div[2]/div/div/section[@class='lemon--section__373c0__fNwDM border-color--default__373c0__3-ifU']/div/div[@class='lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU']/div/div/p[@class='lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-'])[1]/a/text()").get()
        #     web_link=f"https://www.yelp.com{weblink}"
        # except:
        #     web_link = "NA"
        # try:
        #     webname=response_obj.xpath("(//*[@id='wrap']/div[4]/div/div[@class='lemon--div__373c0__1mboc margin-t3__373c0__1l90z margin-b6__373c0__2Azj6 border-color--default__373c0__3-ifU']/div/div/div[2]/div[2]/div/div/section[@class='lemon--section__373c0__fNwDM border-color--default__373c0__3-ifU']/div/div[@class='lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU']/div/div/p[@class='lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-'])[1]/a/@href").get()
        # except:
        #     webname="NA"
        # try:
        #     map_link = response_obj.xpath("(//*[@id='wrap']/div[4]/div/div[@class='lemon--div__373c0__1mboc margin-t3__373c0__1l90z margin-b6__373c0__2Azj6 border-color--default__373c0__3-ifU']/div/div/div[2]/div[2]/div/div/section[@class='lemon--section__373c0__fNwDM border-color--default__373c0__3-ifU']/div/div[@class='lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU']/div/div/p[@class='lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-'])[3]/a/@href").get()
        #     direction=f"https://www.yelp.com{map_link}"
        # except:
        #     direction="NA"



        #
        # try:
        #     checkpoint1=response_obj.xpath("(//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div/div/div[2]/p[2])[1]/a/text()").get()
        # except:
        #     checkpoint1 = None
        # try:
        #     checkpoint2 = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[2]/div/div[1]/div/div[2]/p[2]/a/text()").get()
        # except:
        #     checkpoint2 = None
        #
        #
        # if (checkpoint1 == None and checkpoint2 == None):
        #     try:
        #         name=response_obj.xpath("//h1/text()").get()
        #     except:
        #         name="NA"
        #     try:
        #         direction = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div[2]/div/div[2]/p/a/@href").get()
        #     except:
        #         direction = "NA"
        #     try:
        #         web_link = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div[1]/div/div[2]/p[2]/a/@href").get()
        #     except:
        #         web_link = "NA"
        #     try:
        #         webname = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div[1]/div/div[2]/p[2]/a/text()").get()
        #     except:
        #         webname = "NA"
        #     try:
        #         phone = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div[1]/div/div[2]/p[2]/text()").get()
        #     except:
        #         phone = "NA"
        #
        # elif (checkpoint1 == None):
        #     try:
        #         name=response_obj.xpath("//h1/text()").get()
        #     except:
        #         name = "NA"
        #     try:
        #         direction = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section/div/div[3]/div/div[2]/p/a/@href").get()
        #     except:
        #         direction="NA"
        #     try:
        #         web_link = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[2]/div/div[1]/div/div[2]/p[2]/a/@href").get()
        #     except:
        #         web_link = "NA"
        #     try:
        #         webname = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[2]/div/div[1]/div/div[2]/p[2]/a/text()").get()
        #     except:
        #         webname = "NA"
        #     try:
        #         phone = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[2]/div/div[2]/div/div[2]/p[2]/text()").get()
        #     except:
        #         phone = "NA"
        #
        # else:
        #
        #     try:
        #         name=response_obj.xpath("//h1/text()").get()
        #     except:
        #         name = "NA"
        #     try:
        #         direction = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section/div/div[3]/div/div[2]/p/a/@href").get()
        #     except:
        #         direction = response_obj.xpath("//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section/div/div[3]/div/div[2]/p/a/@href").get()
        #     try:
        #         web_link = response_obj.xpath("(//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div/div/div[2]/p[2])[1]/a/@href").get()
        #     except:
        #         web_link = "NA"
        #     try:
        #         webname = response_obj.xpath("(//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div/div/div[2]/p[2])[1]/a/text()").get()
        #     except:
        #         webname="NA"
        #     try:
        #         phone = response_obj.xpath("(//*[@id='wrap']/div[4]/div/div[3]/div/div/div[2]/div[2]/div/div/section[1]/div/div/div/div[2]/p[2])[2]/text()").get()
        #     except:
        #         phone="NA"



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





        print()
        print(name)
        print(direction)
        print(web_link)
        print(webname)
        print(phone)
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



        Yelpdetails_Item['Name'] = name
        Yelpdetails_Item['website_link'] = web_link
        Yelpdetails_Item['website_name'] = webname
        Yelpdetails_Item['phone'] = phone
        Yelpdetails_Item['Direction'] = direction
        yield Yelpdetails_Item
        page.pop(0)
        if len(page)!=0:
            a=page[0]
            yield SeleniumRequest(
                url=a,
                wait_time=3,
                screenshot=True,
                callback=self.scrapepages,
                meta={'page': page}
            )




