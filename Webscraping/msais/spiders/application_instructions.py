import scrapy


class ApplicationInstructionsSpider(scrapy.Spider):
    name = "application_instructions"
    allowed_domains = ["msais.eng.ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/apply/"]

    def __init__(self):
        self.seen_links = set()

    def parse(self, response):
        with open("Admission/application_instructions.txt", "w", encoding="utf-8") as f:
            f.write("=== Application Instructions ===\n\n")

            paragraphs = response.xpath('//section//p//text() | //section//p//strong/text()').getall()
            for para in [p.strip() for p in paragraphs if p.strip()]:
                f.write(f"{para}\n")
            f.write("\n")

            list_items = response.xpath('//section//ul/li')
            for li in list_items:
                text = li.xpath('string(.)').get()
                if text and text.strip():
                    f.write(f"- {text.strip()}\n")
            f.write("\n")

            button_link = response.xpath('//a[contains(text(), "Apply Now")]/@href').get()
            if button_link:
                full_link = response.urljoin(button_link)
                f.write(f"Apply Now: {full_link}\n")
                self.seen_links.add(full_link)

            footnote_links = response.xpath('//ol[contains(@class, "wp-block-footnotes")]//a/@href').getall()
            for link in footnote_links:
                full_link = response.urljoin(link)
                if "application-fee-waiver" in full_link:
                    f.write(f"Fee Waiver Info: {full_link}\n")
                    self.seen_links.add(full_link)

        if self.seen_links:
            with open("Important_links.txt", "a", encoding="utf-8") as lf:
                lf.write("\n# From: application_instructions\n")
                for link in sorted(self.seen_links):
                    lf.write(f"{link}\n")
