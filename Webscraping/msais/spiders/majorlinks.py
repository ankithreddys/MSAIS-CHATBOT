import scrapy


class MajorlinksSpider(scrapy.Spider):
    name = "majorlinks"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/"]

    def parse(self, response):
        link_boxes = response.xpath('//div[contains(@class,"navbar")]//a')

        with open("Important_links.txt", "a", encoding="utf-8") as f:
            f.write(f"Links for Webpages (Important)\n\n")

            for box in link_boxes:
                title = box.xpath('.//text()').get()
                url = box.xpath('.//@href').get()

                f.write(f"{title}_url : {url}\n")
