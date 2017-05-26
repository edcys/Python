import scrapy
import re
import time
import random
from upwork.items import UpworkItem  
from scrapy.selector import Selector
from scrapy.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class FirstSpider(scrapy.Spider):
    name = "first"
    def start_requests(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.upwork.com/ab/account-security/login")

        elem = self.driver.find_element_by_xpath('//*[@id="login_username"]')
        elem.send_keys("YOUR_USERNAME") # Change this!

        time.sleep(2)
        elem = self.driver.find_element_by_xpath('//*[@id="login_password"]')
        elem.send_keys("YOUR_PASSWORD") # Change this!

        time.sleep(2)
        elem.send_keys(Keys.RETURN)

        time.sleep(20) # Allow you to handle the captcha manually

        headers = {
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
            'accept-encoding':'gzip, deflate, sdch, br',
            'accept-language':'en-US,en;q=0.8',
            'cookie':'device_view=full; _pxvid=086e9820-3a80-11e7-85c4-5fab6341a2f4; _vhipo=2; bfLead=33445ldc7s0g0; __troRUID=5d5a7c3e-cc04-4759-a70d-c08cec1696d3; __ssid=e418988b-94e7-4ba2-81dd-f1b987e500c4; _sp_id.ee6a=c9dce39cc13defad.1495019876.1.1495019876.1495019876; regSuccessWaitTime=%7B%22total%22%3A%2217.7%22%2C%22ga%22%3A%220.3%22%7D; optimizelyEndUserId=oeu1494970718023r0.3175977999075592; _ga=GA1.1.1470705385.1494970724; __ar_v4=BH4WDBCWWJASRDFSPJ6ED5%3A20170516%3A12%7CCQEDEVZYOFD3LDY3DA4C2E%3A20170516%3A12%7CU5TO3O55FJEOTMQ6LLRG7H%3A20170516%3A12; _ceg.s=oq903h; _ceg.u=oq903h; __cfduid=daa4c51ce933f9ad0494fb2c2bc021db91495553415; freelancers-viewed=%5B11263958%2C3389750%2C5624087%2C1059600%2C9388923%2C8669463%2C371204%2C7704506%2C8607222%2C13107817%2C3497385%2C7877888%2C8969843%2C10020115%2C8170172%2C7949142%2C10886092%2C2719911%2C4388472%2C277206%2C1936859%2C1393505%2C7890062%2C10060423%2C8480178%5D; sc.ASP.NET_SESSIONID=zmaowgu4xj1qvk0jdkyatfia; ki_t=1495018332417%3B1495552782764%3B1495553601055%3B7%3B60; ki_r=; __zlcmid=gZgS476XHvKc2Q; company_id=jb1b3l4xywfukkkprfzq0g; current_organization_uid=864802137095147520; company_last_accessed=4048424; recognized=1; session_id=d8c782bab993abe6dd5966a4142b8bba; mp_mixpanel__c=4; optimizelySegments=%7B%222772971468%22%3A%22false%22%2C%222800491501%22%3A%22gc%22%2C%222801081125%22%3A%22referral%22%2C%222806681009%22%3A%22none%22%2C%222853391793%22%3A%22true%22%2C%222877800604%22%3A%22true%22%7D; optimizelyPPID=864802136535633920; optimizelyBuckets=%7B%7D; visitor_id=144.82.8.52.1494970718516968; qt_visitor_id=144.82.8.52.1494970718516968; XSRF-TOKEN=0008663858ddea441a0d5a08644bc30b; _ga=GA1.2.1470705385.1494970724; _gid=GA1.2.680438393.1495629383; _br_uid_2=uid%3D4362760369521%3Av%3D11.8%3Ats%3D1495018331317%3Ahc%3D87; mp_fdf88b8da1749bafc5f24aee259f5aa4_mixpanel=%7B%22distinct_id%22%3A%20%2215c1609911c1c-038d810f55d303-30627509-13c680-15c1609911dc1%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.upwork.com%2Fcat%2Fdevelopers%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.upwork.com%22%7D; _px3=18a6ba2bd38d5b3fa1af724487d522f66946bfca4e15b8448c4efc8ccd109c9f:jEBq3akjywgigFtTevwR9j+YvoiHkQBRijWy1yjiowmr4Xzc5xrYptheCFwQ9MskuV541C+Am+iWmQYXyTIfaQ==:1000:73QdOH7aEDXxYExUkszngQ30zSj2+JojkEUCdMqeBSYR3eC8c8QAgqu3bb2ydiB3BW/JxjwcOTVajW70blCb7fCcWVVPKHVsWn0JKa7zj5se9qNH4orTfwJk4El6orh+OFmD1cZscxUZqKwOOT93d22xC9Gv/auu4EV+eclj/yc=',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Referer':'https://www.upwork.com',
        }
        page_urls = [
            'https://www.upwork.com/o/profiles/browse/?loc=china&q=china',
            # 'https://www.upwork.com/o/profiles/browse/?loc=china&page=266&q=china',
        ]
        for url in page_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)


    # Extract profile links
    def parse(self, response):
        profile_href = response.xpath('//a[@data-log-label="tile_image"]/@href').extract()
        
        for link in profile_href:
            profile_url = response.urljoin(link)
            item = UpworkItem()  

            self.driver.get(profile_url)
            time.sleep(3)
            selector = Selector(text=self.driver.page_source)

            item['profile_link'] = profile_url
            item['image_link'] = selector.xpath('//*[@id="userPortrait"]/@src').extract_first()
            item['name'] = selector.xpath('//*[@id="userPortrait"]/@alt').extract_first()
            item['overview'] = selector.xpath('//*[@id="optimizely-overview-tst1"]/o-profile-overview/section/p/span/span[3]/text()').extract_first()
            
            item['skills'] = re.findall('prettyName\"\:\"(.*?)\"', selector.extract())
            item['priceperhr'] = selector.xpath('//span[@itemprop="pricerange"]/text()').extract_first()


            head_title = selector.xpath('//head/title').extract_first()
            try:
                item['occupation'] = re.findall('\-\s(.*?)\s\-', head_title)[0]
            except Exception:
                pass

            try:
                item['location'] = re.findall('from\s(.*?)\\n', head_title)[0]
            except Exception:
                pass

            
            right_column = selector.xpath('//*[@id="oProfilePage"]/div[2]')
            try:
                item['job_success_rate'] = right_column.xpath('./section[2]/h5/o-job-success/div/div/span/text()').extract_first()[:3]
            except Exception:
                pass
            try:
                item['hours_worked'] = re.findall('\\n(.*?)\shours', right_column.xpath('./section[2]/div/div[1]/text()').extract_first())[0]
            except Exception:
                pass

            try:
                item['jobs_count'] = re.findall('\\n(.*?)\sjobs', right_column.xpath('./section[2]/div/div[2]/text()').extract_first())[0]
            except Exception:
                pass

            try:
                item['earnings'] = re.findall('\\n(.*?)\searned', right_column.xpath('./section[2]/div/div[3]/text()').extract_first())[0]
            except Exception:
                pass

            try:
                item['availablity'] = right_column.xpath('./div[3]/up-dev-availability/div/div[1]/span/text()').extract_first()
            except Exception:
                pass

            try:
                item['availablity_time'] = right_column.xpath('./div[3]/up-dev-availability/div/div[2]/span/text()').extract_first()
            except Exception:
                pass

            try:
                item['response_time'] = right_column.xpath('./div[3]/div/div/span[1]/text()').extract_first()
            except Exception:
                pass

            try:
                item['language'] = right_column.xpath('./o-profile-languages/div').extract_first()
            except Exception:
                pass
                
            
            try:
                item['work_history_and_feedback'] = selector.xpath('//*[@id="oProfileAssignments"]/div/div/div[2]').extract_first()
            except Exception:
                pass

            left_column = selector.xpath('//*[@id="oProfilePage"]/div[1]/div[2]')
            try:
                item['tests'] = left_column.xpath('./o-profile-tests/div').extract_first()
            except Exception:
                pass
            try:
                item['certifications'] = left_column.xpath('./o-profile-certificates/div').extract_first()
            except Exception:
                pass
            try:
                item['employment_history'] = left_column.xpath('./o-profile-employment-history/div').extract_first()
            except Exception:
                pass
            try:
                item['education'] = left_column.xpath('./o-profile-education/div').extract_first()
            except Exception:
                pass
            try:
                item['other_experiences'] = left_column.xpath('./o-profile-other-experience/div').extract_first()
            except Exception:
                pass
            
            # try:
                
            # except Exception:
            #     pass

            yield item

        if response.url != 'https://www.upwork.com/o/profiles/browse/?loc=china&q=china':
            current_page = re.findall('page\=(.*?)\&q', response.url)[0]
            next_page = int(current_page) + 1
            if next_page > 500:
                driver.close()
            next_page = 'https://www.upwork.com/o/profiles/browse/?loc=china&page=%s&q=china' % next_page
        else:
            next_page = 'https://www.upwork.com/o/profiles/browse/?loc=china&page=2&q=china'
        
        print('------Finish a page------')
        time.sleep(10)
        print('------Go to next page------')
        yield scrapy.Request(url=next_page, callback=self.parse)







        

