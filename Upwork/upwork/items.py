# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# mongoexport -h 127.0.0.1 -d Upwork -c UpworkDoc -f name,location,occupation,skills,priceperhr,hours_worked,jobs_count,job_success_rate,earnings,availablity,availablity_time,response_time,profile_link,image_link,overview,language,work_history_and_feedback,tests,certifications,employment_history,education,other_experiences --csv -o test_2.csv

import scrapy


class UpworkItem(scrapy.Item):
    # define the fields for your item here like:
    profile_link = scrapy.Field()
    image_link = scrapy.Field()
    name = scrapy.Field()
    overview = scrapy.Field()
    
    skills = scrapy.Field()
    priceperhr = scrapy.Field()
    occupation = scrapy.Field()
    location = scrapy.Field()

    # Right column
    job_success_rate = scrapy.Field()
    hours_worked = scrapy.Field()
    jobs_count = scrapy.Field()
    earnings = scrapy.Field()
    availablity = scrapy.Field()
    availablity_time = scrapy.Field()
    response_time = scrapy.Field()

    language = scrapy.Field()
    work_history_and_feedback = scrapy.Field()
    tests = scrapy.Field()
    certifications = scrapy.Field()
    employment_history = scrapy.Field()
    education = scrapy.Field()
    other_experiences = scrapy.Field()
    pass

