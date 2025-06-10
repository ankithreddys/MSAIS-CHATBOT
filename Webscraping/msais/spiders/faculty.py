import scrapy
import os


class FacultySpider(scrapy.Spider):
    name = "faculty"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/faculty/"]

    def parse(self, response):
        container = response.xpath('//div[@class="site-content"]')

        header = container.xpath('.//h2//text()').get()
        intro = container.xpath('.//div[contains(@class,"9d6595d7")]//p//text()').getall()
        intro_text = ' '.join([text.strip() for text in intro if text.strip()])

        with open("People/faculty.txt", "w", encoding="utf-8") as f:
            f.write(f"{header}\n\n")
            f.write("Intro:\n" + intro_text + "\n\n")
            f.write("Faculty List:\n\n")

            faculty_cards = container.xpath('.//div[contains(@class,"cards__item")]')

            for card in faculty_cards:
                name = card.xpath('.//h3/text()').get()
                department = card.xpath('.//div[contains(@class,"demo-author-block-acf__innerblocks")]/p/text()').get()
                profile_url = card.xpath('.//a[@class="card-link"]/@href').get()

                if name and department and profile_url:
                    f.write(f"Name: {name.strip()}\n")
                    f.write(f"Department: {department.strip()}\n")
                    f.write(f"Profile URL: {response.urljoin(profile_url)}\n\n")
