import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class A6pmSpider(CrawlSpider):
    name = "6pm"
    allowed_domains = ["www.6pm.com"]
    start_urls = ["https://www.6pm.com/"]
    scrapped_retailer_skus = set()

    rules = (
        Rule(LinkExtractor(restrict_css='[data-sub-nav="true"] a.fi-z')),
        Rule(LinkExtractor(restrict_css='[id="searchPagination"] a')),
        Rule(LinkExtractor(restrict_css='[id="products"] a[itemprop="url"]'), callback="parse_item"),
    )

    def parse_item(self, response):
        retailer_sku = self.extract_retailer_sku(response)
        if self.is_sku_already_scrapped(retailer_sku):
            return

        item_data = {
            "retailer_sku": retailer_sku,
            "gender": self.extract_item_gender(response),
            "brand": self.extract_item_brand(response),
            "category": response.css("div#breadcrumbs a::text").extract()[1:],
            "url": response.url,
            "name": response.css("span.Ws-z::text").get(),
            "description": response.css("div[itemprop='description'] ul").get(),
            "currency": response.css('span[itemprop="priceCurrency"]::attr(content)').get(),
            "skus": self.extract_item_skus(response),
        }
        yield item_data

    def extract_retailer_sku(self, response):
        retailer_sku = response.css('span[itemprop="sku"]::text').get()
        return retailer_sku

    def extract_item_gender(self, response) -> str:
        keywords = response.css('meta[name="keywords"]::attr(content)').get().lower()
        if "women" in keywords and "men" not in keywords:
            gender = "women"
        elif "men" in keywords and "women" not in keywords:
            gender = "men"
        elif "men" in keywords and "women" in keywords:
            gender = "unisex-adults"
        elif "girls" in keywords and not "boys" in keywords:
            gender = "girls"
        elif "boys" in keywords and not "girls" in keywords:
            gender = "boys"
        elif "boys" in keywords and "girls" in keywords:
            gender = "unisex-kids"
        else:
            gender = "unisex-adults"
        return gender

    def extract_item_brand(self, response) -> dict:
        brand_css = "span[itemprop='brand'] span[itemprop='name']::text"
        logo_css = "img[itemprop='logo']::attr(src)"
        return {
            "name": response.css(brand_css).get(),
            "logo": response.css(logo_css).get(),
        }

    def extract_item_skus(self, response) -> dict:
        initial_state_str = response.xpath('//script[contains(., "window.__INITIAL_STATE__")]/text()').get()
        initial_state_str = re.sub(r";|window.__INITIAL_STATE__ = ", "", initial_state_str)
        initial_state_json = json.loads(initial_state_str)
        product_json = initial_state_json.get("product").get("detail")
        color_versions = product_json.get("styles")
        skus_data = {}

        for color_version in color_versions:
            color = color_version.get("color")
            size_versions = color_version.get("stocks")
            images = color_version.get("images")
            image_urls = [
                f'https://m.media-amazon.com/images/I/{image["imageId"]}._AC_SR146,116_.jpg' for image in images
            ]
            skus_data[color] = {"image_urls": image_urls, "size_versions": {}}
            for size_version in size_versions:
                size = size_version.get("size")
                out_of_stock = int(size_version.get("onHand")) <= 0
                skus_data[color]["size_versions"][size] = {
                    "sku_id": size_version.get("stockId"),
                    "price": size_version.get("price").replace("$", ""),
                    "previous_price": size_version.get("originalPrice").replace("$", ""),
                    "out_of_stock": out_of_stock,
                }
        return skus_data

    def is_sku_already_scrapped(self, retailer_sku):
        if retailer_sku in self.scrapped_retailer_skus:
            return True

        self.scrapped_retailer_skus.add(retailer_sku)
