# import scrapy


# class HomepageSpider(scrapy.Spider):
#     name = "homepage"
#     allowed_domains = ["www.ufl.edu"]
#     start_urls = ["https://msais.eng.ufl.edu/"]

#     def parse(self, response):
#         news_box = response.xpath('//div[contains(@class,"slider-manual")]')
#         page_title = news_box.xpath('.//h2//text()').get()

#         # Yield the overall title (once)
#         yield {
#             'Title': page_title.strip() if page_title else "N/A"
#         }

#         news_list = news_box.xpath('.//a')
#         for news in news_list:
#             news_title = news.xpath('.//p[@class="slide-title mb-3"]/text()').get()
#             news_title = news_title.strip() if news_title else "N/A"

#             news_text_parts = news.xpath('.//p[@class="slide-subtext"]//text()').getall()
#             news_text = ' '.join(part.strip() for part in news_text_parts if part.strip())

#             yield {
#                 'News Title': news_title,
#                 'Text': news_text
#             }


import scrapy


class HomepageSpider(scrapy.Spider):
    name = "homepage"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/"]

    def parse(self, response):
        news_box = response.xpath('//div[contains(@class,"slider-manual")]')
        page_title = news_box.xpath('.//h2//text()').get()

        with open("About/homepage.txt", "w", encoding="utf-8") as f:
            if page_title:
                f.write(f"Page Title: {page_title.strip()}\n\n")

            news_list = news_box.xpath('.//a')
            for idx, news in enumerate(news_list):
                news_title = news.xpath('.//p[@class="slide-title mb-3"]/text()').get()
                news_title_clean = news_title.strip() if news_title else f"Untitled News #{idx + 1}"

                news_text_parts = news.xpath('.//p[@class="slide-subtext"]//text()').getall()
                news_text = ' '.join(part.strip() for part in news_text_parts if part.strip())

                f.write(f"--- News {idx + 1} ---\n")
                f.write(f"{news_title_clean}\n")
                f.write(f"{news_text}\n\n")

