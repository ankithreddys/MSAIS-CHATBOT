import scrapy


class CurriculamCommitteeSpider(scrapy.Spider):
    name = "curriculam_committee"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/curriculum-committee/"]

    def parse(self, response):
        with open("People/faculty_combined.txt", "w", encoding="utf-8") as f:

            f.write("=== Faculty Visual Navigation ===\n\n")
            cards = response.xpath('//a[contains(@class, "visual-navigation-link")]')

            for card in cards:
                profile_url = card.xpath('./@href').get()
                image_alt = card.xpath('.//img/@alt').get(default="")
                paragraph = card.xpath('.//p//text()').get(default="").strip()

                if image_alt:
                    parts = [part.strip() for part in image_alt.split("<br>") if part.strip()]
                    name_role = parts[0] if len(parts) > 0 else "N/A"
                    research = parts[1] if len(parts) > 1 else "N/A"
                else:
                    name_role = paragraph.split("Primary Research Area")[0].strip()
                    research = paragraph if "Primary Research Area" in paragraph else "N/A"

                f.write(f"Name/Role: {name_role}\n")
                f.write(f"Primary Research Area: {research.replace('Primary Research Area:', '').strip()}\n")
                f.write(f"Profile URL: {response.urljoin(profile_url)}\n\n")


            f.write("=== Academic Advisor and Representatives ===\n\n")
            sections = response.xpath('//div[contains(@class,"wp-block-column")]')

            for section in sections:
                titles = section.xpath('.//p/strong/text()').getall()
                uls = section.xpath('.//ul')

                for title, ul in zip(titles, uls):
                    members = ul.xpath('.//li/text()').getall()
                    members = [m.strip() for m in members if m.strip()]
                    f.write(f"{title.strip()}:\n\n")
                    for member in members:
                        f.write(f"{member}\n")
                    f.write("\n")

