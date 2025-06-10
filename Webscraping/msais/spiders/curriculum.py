import scrapy


class CurriculumSpider(scrapy.Spider):
    name = "curriculum"
    allowed_domains = ["msais.eng.ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/curriculum/"]

    def __init__(self):
        self.seen_links = set()

    def parse(self, response):
        with open("Academics/Curriculum.txt", "w", encoding="utf-8") as f:
            f.write("=== Degree Requirements & Curriculum ===\n\n")

            degree_section = response.xpath('//h2[contains(text(), "Degree Requirements")]/ancestor::section[1]')
            if degree_section:
                f.write("--- Degree Requirements ---\n")
                paras = degree_section.xpath('.//p//text()').getall()
                for para in [p.strip() for p in paras if p.strip()]:
                    f.write(f"{para}\n")
                f.write("\n")

                list_items = degree_section.xpath('.//ul/li')
                for li in list_items:
                    text = li.xpath('string(.)').get()
                    if text and text.strip():
                        f.write(f"- {text.strip()}\n")

                image_url = degree_section.xpath('.//img/@src').get()
                if image_url:
                    full_img = response.urljoin(image_url)
                    f.write(f"\nCurriculum Flowchart Image: {full_img}\n")
                    self.seen_links.add(full_img)

                f.write("\n")

            f.write("--- Curriculum (4 Semesters) ---\n")
            semesters = response.xpath('//div[contains(@class,"accordion-item")]')
            for semester in semesters:
                title = semester.xpath('.//button[contains(@class,"accordion-button")]/text()').get()
                if title:
                    f.write(f"\n>> {title.strip()} <<\n")

                list_items = semester.xpath('.//ul/li')
                for li in list_items:
                    text = li.xpath('string(.)').get()
                    if text and text.strip():
                        f.write(f"- {text.strip()}\n")

                para_lines = semester.xpath('.//p//text()').getall()
                for line in [p.strip() for p in para_lines if p.strip()]:
                    f.write(f"{line}\n")

                links = semester.xpath('.//a/@href').getall()
                for link in links:
                    full_link = response.urljoin(link)
                    f.write(f"Link: {full_link}\n")
                    self.seen_links.add(full_link)

        if self.seen_links:
            with open("Important_links.txt", "a", encoding="utf-8") as lf:
                lf.write("\n# From: degree_curriculum\n")
                for link in sorted(self.seen_links):
                    lf.write(f"{link}\n")
