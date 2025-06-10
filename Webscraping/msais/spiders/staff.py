import scrapy
import os


class StaffSpider(scrapy.Spider):
    name = "staff"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/staff/"]

    def parse(self, response):
        os.makedirs("People", exist_ok=True)

        container = response.xpath('//div[contains(@class,"content-area")]')

        header = container.xpath('.//h2/text()').get(default="Staff").strip()

        intro_parts = container.xpath('//p[@class="intro"]//text()').getall()
        intro_text = ' '.join([part.strip() for part in intro_parts if part.strip()])

        with open("People/Staff.txt", mode="w", encoding="utf-8") as f:
            f.write(f"{header}\n\n")
            f.write("Intro:\n" + intro_text + "\n\n")

            cards = container.xpath('.//div[contains(@class,"cards__item")]')
            for card in cards:
                name = card.xpath('.//h3/text()').get(default="N/A").strip()

                roles = card.xpath('.//p[1]//text()').getall()
                role = '\n'.join([r.strip() for r in roles if r.strip()])

                contact_details = card.xpath('.//p[2]//text()').getall()
                contact_text = '\n'.join([cd.strip() for cd in contact_details if cd.strip()])

                f.write(f"Name : {name}\n")
                f.write(f"Role : {role}\n")
                f.write(f"Contact:\n{contact_text}\n\n")
