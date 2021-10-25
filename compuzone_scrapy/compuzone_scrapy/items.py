# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CompuzoneScrapyPipeline(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    origin = scrapy.Field()
    manufacturer = scrapy.Field()
    id = scrapy.Field()
    price = scrapy.Field()
    title_image = scrapy.Field()
    detail_image = scrapy.Field()
    delivery_fee = scrapy.Field()    
    
class Category(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()