import scrapy


class FinancialInformationSpider(scrapy.Spider):
    name = "financial_information"
    allowed_domains = ["msais.eng.ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/financial-information/"]

    def __init__(self):
        self.seen_links = set()

    def parse(self, response):
        with open("Admission/Financial Information.txt", "w", encoding="utf-8") as f:
            f.write("=== Funding Information ===\n\n")

            intro = response.xpath('//h2[contains(text(), "Funding")]/following-sibling::p[1]/text()').get()
            if intro:
                f.write(f"{intro.strip()}\n\n")

            accordion_items = response.xpath('//div[contains(@class, "accordion-item")]')
            for item in accordion_items:
                heading = item.xpath('.//h3/text()').get()
                if heading:
                    f.write(f"--- {heading.strip()} ---\n")

                text_lines = item.xpath('.//div[contains(@class, "tab-body-wrap")]//p//text() | .//div[contains(@class, "tab-body-wrap")]//p//strong/text()').getall()
                for line in [l.strip() for l in text_lines if l.strip()]:
                    f.write(f"{line}\n")

                links = item.xpath('.//a/@href').getall()
                for link in links:
                    full_link = response.urljoin(link)
                    f.write(f"Link: {full_link}\n")
                    self.seen_links.add(full_link)

                f.write("\n")

        if self.seen_links:
            with open("Important_links.txt", "a", encoding="utf-8") as lf:
                lf.write("\n# From: Financial Information\n")
                for link in sorted(self.seen_links):
                    lf.write(f"{link}\n")
