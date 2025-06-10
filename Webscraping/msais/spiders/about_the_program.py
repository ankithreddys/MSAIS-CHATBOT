import scrapy


class AboutTheProgramSpider(scrapy.Spider):
    name = "about_the_program"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/about-the-program/"]

    def parse(self, response):
        main_page = response.xpath('//div[contains(@class,"site-content")]')

        title = main_page.xpath('.//h2//text()').get(default="No Title").strip()

        raw_content = main_page.xpath('.//p//text()').getall()
        page_content = '\n'.join([p.strip() for p in raw_content if p.strip()])

        links = main_page.xpath('.//a')
        formatted_links = []

        for link in links:
            text = link.xpath('.//text()').get()
            href = link.xpath('.//@href').get()

            if text and href:
                clean_text = text.strip().replace('\n', '')
                full_url = response.urljoin(href.strip())
                formatted_links.append(f"{clean_text}: {full_url}")

        with open("Important_links.txt", "a", encoding="utf-8") as f_links:
            f_links.write("\n\n# About the Program Links\n")
            for line in formatted_links:
                f_links.write(line + "\n")

        with open("About/About_Program_Content.txt", "w", encoding="utf-8") as f_content:
            f_content.write(f"Title: {title}\n\n")
            f_content.write("Page Content:\n")
            f_content.write(page_content + "\n")
