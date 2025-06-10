import scrapy


class ApplicationFeeWaiverSpider(scrapy.Spider):
    name = "application_fee_waiver"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/application-fee-waiver/"]

    def __init__(self):
        self.seen_links = set()

    def parse(self, response):
        with open("Admission/application_fee_waiver.txt", "w", encoding="utf-8") as f:
            title = response.xpath('//section//h2[contains(text(), "Application Fee Waiver")]/text()').get()
            if title:
                f.write(f"=== {title.strip()} ===\n\n")

            paragraphs = response.xpath('//section//p//text()').getall()
            for para in [p.strip() for p in paragraphs if p.strip()]:
                f.write(f"{para}\n")
            f.write("\n")

            subsections = response.xpath('//section[contains(@class, "wp-block-create-block-announcements-showcase")]')
            for subsection in subsections:
                heading = subsection.xpath('.//h2/text()').get()
                if heading:
                    f.write(f"--- {heading.strip()} ---\n")

                text_lines = subsection.xpath('.//p//text()').getall()
                for line in [t.strip() for t in text_lines if t.strip()]:
                    f.write(f"{line}\n")

                links = subsection.xpath('.//a/@href').getall()
                for link in links:
                    full_link = response.urljoin(link)
                    f.write(f"Link: {full_link}\n")
                    self.seen_links.add(full_link)

                f.write("\n")

        with open("Important_links.txt", "a", encoding="utf-8") as lf:
            lf.write("=== Unique Important Links Found ===\n\n")
            for link in sorted(self.seen_links):
                lf.write(f"{link}\n")
