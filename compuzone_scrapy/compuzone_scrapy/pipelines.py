# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter

class CompuzoneScrapyPipeline:
    
    def open_spider(self, spider):
        self.file = open('items.json', 'w', encoding='utf-8')
        # header = '{'
        # self.file.write(header)
        
    def close_spider(self, spider):
        # footer = '}'
        # self.file.write(footer)
        self.file.close()
        
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
