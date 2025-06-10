import scrapy


class AdministrationSpider(scrapy.Spider):
    name = "administration"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/administration/"]

    def parse(self, response):
        container = response.xpath('//div[contains(@class,"wp-container-core")]')

        header = container.xpath('.//h2/text()').get(default='').strip()

        intro_paragraphs = container.xpath('.//p[not(ancestor::div[contains(@class,"faculty-bio")])]/text()').getall()
        intro_text = '\n'.join([p.strip() for p in intro_paragraphs if p.strip()])

        name = container.xpath('.//div[@class="faculty-contact-info"]/p[1]/text()').get(default='').strip()
        role = container.xpath('.//div[@class="faculty-contact-info"]/p[2]/text()').get(default='').strip()
        phone = container.xpath('.//a[contains(@class, "faculty-tel")]/text()').get(default='').strip()
        email = container.xpath('.//a[contains(@class, "faculty-email")]/@href').get(default='')
        email = email.replace("mailto:", "") if email else ""

        bio_paragraphs = container.xpath('.//div[@class="wp-block-create-block-faculty-bio-right"]//p//text()').getall()
        bio_text = '\n'.join([p.strip() for p in bio_paragraphs if p.strip()])


        with open("People/administration_Coordinator_Info.txt", "w", encoding="utf-8") as f:
            f.write(f"{header}\n\n")
            f.write("Intro:\n" + intro_text + "\n\n")
            f.write("Name: " + name + "\n")
            f.write("Role: " + role + "\n")
            f.write("Phone: " + phone + "\n")
            f.write("Email: " + email + "\n")
            f.write("Bio:\n" + bio_text + "\n")
