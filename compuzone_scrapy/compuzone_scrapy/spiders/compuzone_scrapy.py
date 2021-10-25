from scrapy import Request, Spider
from re import findall as rfindall
from compuzone_scrapy.items import CompuzoneScrapyPipeline

class CompuzoneScrapingSpider(Spider):
    name = 'compuzone_scrapy'
    start_urls = ['https://compuzone.co.kr/main/main.htm']
    base_url = 'https://compuzone.co.kr'
    
    # privoxy main configuration.txt
    #     # forward-socks5 / 127.0.0.1:9150 .
    #     # forward-socks4a / 127.0.0.1:9150 .
        
    #     self.proxies = {
    #         'http': 'socks5://127.0.0.1:9150',
    #         'https': 'socks5://127.0.0.1:9150'
    #     }

    def parse(self, response):
        # category_name = response.xpath('//*[@class="BigDivLi"]/a/text()').extract()
        category_url = response.xpath('//*[@class="BigDivLi"]/a/@href').extract()
        # for curl in category_url:
        #     yield Request(url=curl, callback=self.move_to_product_page)
        yield Request(url="https://compuzone.co.kr/product/productB_new_list.htm?BigDivNo=3", callback=self.parse_category_page)
        
        
    def parse_category_page(self, response):
        product_num = response.xpath('//*[@id="ProductList"]/div[1]/h2/span/text()').extract()[0]
        product_num = rfindall('\d+', product_num)
        product_num = int(''.join(product_num))
        for page_count, product_count in enumerate(range(0, product_num, 60)):
            category_page = response.request.url + '&PageCount=60' + '&StartNum=' + str(product_count) + '&PageNum=' + str(page_count+1)
            yield Request(url=category_page, callback=self.parse_product_page)
    
    def parse_product_page(self, response):
        product_page_url = response.xpath('//div[@class="prd_img"]/a/@href').extract()
        for product_page in product_page_url:
            yield Request(url=product_page, callback=self.parse_item)
    
    def parse_item(self, response):
        item = CompuzoneScrapyPipeline()
        item['category'] = response.xpath('//*[@id="product_navi"]/ul/li[2]/a/text()').extract()[0]
        item['name'] = response.xpath('//*[@class="pdtl_col_top"]/h2/text()').extract()[0].strip()
        item['origin'] = response.xpath('//*[@class="pddt_info_area pddt_info_area1"]/table/tr[contains(.,"제조국")]/td[2]/text()').extract()
        item['manufacturer'] = response.xpath('//*[@class="pddt_info_area pddt_info_area1"]/table/tr[contains(.,"제조자/수입자")]/td[1]/text()').extract()
        product_id = response.xpath('//*[@class="p_num"]/text()').extract()[0]
        item['id'] = [s for s in rfindall(r'-?\d+\.?\d*', product_id)][0]
        product_price = response.xpath('//*[@class="price_real"]/text()').extract()[1].strip()
        item['price'] = ''.join([s for s in rfindall(r'-?\d+\.?\d*', product_price)])
        item['title_image'] = response.xpath('//*[@id="mainImg_1"]/img/@src').extract()[0]
        item['detail_image'] = response.xpath('//*[@id="pdtl_detail_img"]/div/table/tr//img/@src').extract()
        try:
            delivery_fee = response.xpath('//*[@class="pd delivery_price"]/div/p/text()').extract()[0].strip()
        except:
            delivery_fee = '정보 없음'
        item['delivery_fee'] = delivery_fee   
        yield item
        