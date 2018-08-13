# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import sys
import re

class IuEmailScrapingySpider(scrapy.Spider):
    name = 'iu_email_scrapingy'
    allowed_domains = ['directory.iu.edu/']
    start_urls = ['https://directory.iu.edu/']

    def parse(self, response):
        requestVerificationToken = response.xpath("//*[@id='directoryForm']/input/@value").extract_first()
        yield FormRequest.from_response(response,
                                        formdata = {
                                            "__RequestVerificationToken": requestVerificationToken,
                                            "SearchText": "abigail t",
                                            "Campus": "BL",
                                            "Affiliation": "Student",
                                            "IncludeDepartmentListings": "false",
                                            "ExactMatch": "false"
                                        },
                                        dont_filter = True,
                                        formxpath = "//*[@id='directoryForm']",
                                        callback = self.parse_search)

    def parse_search(self, response):
        # resultsList = response.xpath("//*[@id='content']/div[1]/div/section[3]/div/div[1]/div/div[2]/div[2]/ul/")
        # print resultsList
        resultScript = response.xpath("//head/script[@type='text/javascript']").extract_first()
        # resultsList = resultScript.split("search",1)[1])
        result = re.search('searchResultItemList: (.*)', resultScript)
        final = result.group(1)
        yield {"resultList" : final}