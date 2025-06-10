import scrapy


class AcademicPoliciesSpider(scrapy.Spider):
    name = "academic_policies"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/academic-policies/"]

    def __init__(self):
        self.seen_links = set()

    def parse(self, response):
        with open("Academics/academic_policies.txt", "w", encoding="utf-8") as f:
            f.write("=== Academic Policies & Procedures ===\n\n")

            sections = response.xpath('//section[contains(@class, "fullwidth-text-block")]')
            for section in sections:
                title = section.xpath('.//h2/text()').get()
                if title:
                    f.write(f"--- {title.strip()} ---\n")

                list_items = section.xpath('.//ul//li')
                for li in list_items:
                    text = li.xpath('string(.)').get()
                    if text and text.strip():
                        f.write(f"- {text.strip()}\n")

                links = section.xpath('.//a/@href').getall()
                for link in links:
                    full_link = response.urljoin(link)
                    f.write(f"Link: {full_link}\n")
                    self.seen_links.add(full_link)

                f.write("\n")

        if self.seen_links:
            with open("Important_links.txt", "a", encoding="utf-8") as lf:
                lf.write("\n# From: academic_policies\n")
                for link in sorted(self.seen_links):
                    lf.write(f"{link}\n")
