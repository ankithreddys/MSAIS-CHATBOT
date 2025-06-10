import scrapy


class WhyThisProgramSpider(scrapy.Spider):
    name = "why_this_program"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/why-this-program/"]

    def parse(self, response):
        cards = response.xpath('//a[contains(@class, "button card") and not(contains(@class, "slick-cloned"))]')

        with open("About/why_this_program_cards.txt", "w", encoding="utf-8") as f:
            f.write("Why This Program?\n\n")

            for i, card in enumerate(cards, 1):
                title = card.xpath('.//span[@class="cta-title"]/text()').get()
                text = card.xpath('.//span[@class="cta-text"]/text()').get()

                f.write(f"{title.strip() if title else 'No Title'}:{text.strip() if text else 'No Content'}\n\n")
