import scrapy


class EnglishProficiencySpider(scrapy.Spider):
    name = "english_proficiency"
    allowed_domains = ["msais.eng.ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/english-proficiency-test/"]

    def __init__(self):
        self.seen_links = set()

    def parse(self, response):
        with open("Admission/english_proficiency.txt", "w", encoding="utf-8") as f:
            paragraphs = response.xpath('//section//p//text()').getall()
            for para in [p.strip() for p in paragraphs if p.strip()]:
                f.write(f"{para}\n")
            f.write("\n")

            # Announcements including TOEFL Discount
            announcements = response.xpath('//section[contains(@class, "wp-block-create-block-announcements-showcase")]')
            for block in announcements:
                heading = block.xpath('.//h2/text()').get()
                if heading:
                    f.write(f"--- {heading.strip()} ---\n")

                text_lines = block.xpath('.//p//text() | .//p//strong/text()').getall()
                for line in [l.strip() for l in text_lines if l.strip()]:
                    f.write(f"{line}\n")

                links = block.xpath('.//a/@href').getall()
                for link in links:
                    full_link = response.urljoin(link)
                    f.write(f"Link: {full_link}\n")
                    self.seen_links.add(full_link)

                f.write("\n")

        # Append unique links to shared file
        if self.seen_links:
            with open("Important_links.txt", "a", encoding="utf-8") as lf:
                lf.write("\n# From: english_proficiency\n")
                for link in sorted(self.seen_links):
                    lf.write(f"{link}\n")

