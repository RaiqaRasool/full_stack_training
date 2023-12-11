import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class A6pmSpider(CrawlSpider):
    name = "6pm"
    allowed_domains = ["www.6pm.com"]
    start_urls = ["https://www.6pm.com/"]
    data = {}

    rules = (
        Rule(LinkExtractor(restrict_css = '[data-sub-nav="true"] a.fi-z')),
        Rule(LinkExtractor(restrict_css='[id="searchPagination"] a'), follow=True),
        Rule(LinkExtractor(restrict_css = '[id="products"] a[itemprop="url"]'), callback="parse_item"),
    )

    def parse_item(self, response):
        retailer_sku = self.extract_retailer_sku(response)
        if retailer_sku in self.data:
            return
        item_dict = {
            "retailer_sku": self.extract_retailer_sku(response),
            "gender": self.extract_item_gender(response),
            "brand": {
                "name": response.css("div#breadcrumbs div a:last-child span::text").get(),
                "logo": response.css('a[data-track-value="Brand-Logo"] img::attr(src)').get(),
            },
            "category": response.css("div#breadcrumbs div a::text").extract()[1:],
            "url": response.url,
            "name": response.css("span.Ws-z::text").get(),
            "description": response.css("div[itemprop='description'] div.uV-z ul").get(),
            "currency": response.css("span.fu-z.iu-z span:first-child span:first-child::attr(content)").get(),
            "skus": self.extract_item_skus(response),
        }
        self.data[retailer_sku] = item_dict
        yield item_dict


    def extract_retailer_sku(self, response):
        sku_id = response.css("div[itemprop='description'] div.uV-z ul li:nth-child(2) span::text").get()
        return sku_id

    def extract_item_gender(self, response) -> str:
        keywords = response.css('meta[name="keywords"]::attr(content)').get()
        if "Women" in keywords and "Men" not in keywords:
            gender = "women"
        elif "Men" in keywords and "Women" not in keywords:
            gender = "men"
        elif "Men" in keywords and "Women" in keywords:
            gender = "unisex-adults"
        elif "Girls" in keywords and not "Boys" in keywords:
            gender = "girls"
        elif "Boys" in keywords and not "Girls" in keywords:
            gender = "boys"
        elif "Boys" in keywords and "Girls" in keywords:
            gender = "unisex-kids"
        else:
            gender = "unisex-adults"
        return gender

    def extract_item_skus(self, response) -> dict:
        initial_state_str = response.xpath('//script[contains(., "window.__INITIAL_STATE__")]/text()').get()[27:-1]
        skus_dict = {}
        initial_state_json = json.loads(initial_state_str)
        product_json = initial_state_json.get("product").get("detail")
        color_versions = product_json.get("styles")
        for color_version in color_versions:
            color = color_version.get("color")
            skus = color_version.get("stocks")
            images = color_version.get("images")
            image_urls = []
            for image in images:
                image_urls.append(f'https://m.media-amazon.com/images/I/{image["imageId"]}._AC_SR146,116_.jpg')
            for sku in skus:
                size = sku.get("size")
                sku_key = f"{size}_{color}"
                out_of_stock = True if int(sku.get("onHand")) > 0 else False
                skus_dict[sku_key] = {
                    "sku_id": sku.get("stockId"),
                    "size": size,
                    "color": color,
                    "price": sku.get("price")[1:],
                    "previous_price": sku.get("originalPrice")[1:],
                    "out_of_stock": out_of_stock,
                    "image_urls": image_urls,
                }
        return skus_dict
