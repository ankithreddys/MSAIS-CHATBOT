import scrapy


class RequiredDocumentsDetailedSpider(scrapy.Spider):
    name = "required_documents_detailed"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/preparing-your-packet/"]

    def parse(self, response):
        with open("Admission/required_documents_detailed.txt", "w", encoding="utf-8") as f:
            sections = response.xpath('//section[contains(@class, "fullwidth-text-block")]')

            for section in sections:
                # Get section title
                title = section.xpath('.//h2/text()').get()
                title = title.strip() if title else "General Information"
                f.write(f"\n=== {title} ===\n\n")

                # Write all paragraph content
                paragraphs = section.xpath('.//p//text()').getall()
                for para in [p.strip() for p in paragraphs if p.strip()]:
                    f.write(f"{para}\n")
                f.write("\n")

                # Write all list items
                list_items = section.xpath('.//ul//li')
                for li in list_items:
                    text = li.xpath('string(.)').get()
                    if text and text.strip():
                        f.write(f"- {text.strip()}\n")
                f.write("\n")

                # Write all links
                links = section.xpath('.//a/@href').getall()
                if links:
                    f.write("Links:\n")
                    for link in links:
                        f.write(f"- {response.urljoin(link)}\n")
                    f.write("\n")
