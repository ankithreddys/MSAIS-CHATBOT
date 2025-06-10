import scrapy


class FaqSSpider(scrapy.Spider):
    name = "faq_s"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/frequentlyaskedquestions/"]

    def parse(self, response):
        seen_links = set()

        with open("About/FAQ'S.txt", "w", encoding="utf-8") as f_faq:
            f_faq.write("Title: FAQ'S\n\nPage Content:\n")

        elements = response.xpath('//div[contains(@class, "accordion-item")]')

        for element in elements:
            question = element.xpath('.//button[contains(@class, "accordion-button")]/text()').get(default='').strip()
            answer_parts = element.xpath('.//div[contains(@class,"accordion-body")]//p//text()').getall()
            answer = ' '.join([part.strip() for part in answer_parts if part.strip()])

            links = element.xpath('.//div[contains(@class,"accordion-body")]//a/@href').getall()

            with open("About/FAQ'S.txt", "a", encoding="utf-8") as f_faq:
                f_faq.write(f"\nQ: {question}\n")
                f_faq.write(f"A: {answer}\n")
                if links:
                    f_faq.write("Links:\n")
                    for link in links:
                        f_faq.write(f" - {link}\n")

            with open("Important_links.txt", "a", encoding="utf-8") as f_links:
                for link in links:
                    if link not in seen_links:
                        f_links.write(link + "\n")
                        seen_links.add(link)
