import scrapy
import os
from w3lib.html import remove_tags


class AdmissionRequirementsSpider(scrapy.Spider):
    name = "admission_requirements"
    allowed_domains = ["ufl.edu"]
    start_urls = ["https://msais.eng.ufl.edu/admission-requirements-deadlines/"]

    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_headings = set()
        self.seen_links = set()
        os.makedirs("Admission", exist_ok=True)

    def parse(self, response):
        with open("Admission/Admission_Requirements&Deadlines.txt", "w", encoding="utf-8") as f_text, \
             open("Important_links.txt", "a", encoding="utf-8") as f_links:
            sections = response.xpath('//section[contains(@class, "fullwidth-text-block")]')

            for section in sections:
                heading_parts = section.xpath('.//h2//text() | .//h3//text()').getall()
                heading = ' '.join(part.strip() for part in heading_parts if part.strip()).strip()
                
                if heading and heading not in self.seen_headings:
                    self.seen_headings.add(heading)
                    f_text.write(f"{heading}\n\n")

                paragraphs = section.xpath('.//p')
                for para_node in paragraphs:
                    text = self.extract_text_with_links(para_node, response, f_links)
                    if text:
                        f_text.write(text + "\n")
                
                if paragraphs:
                    f_text.write("\n")

                list_items = section.xpath('.//li')
                for li_node in list_items:
                    text = self.extract_text_with_links(li_node, response, f_links)
                    if text:
                        f_text.write(f"- {text}\n")
                
                if list_items:
                    f_text.write("\n")

    def extract_text_with_links(self, node, response, f_links):
        parts = []

        for sub_node in node.xpath('./node()'):
            if sub_node.xpath('name()').get():
                tag_name = sub_node.xpath('name()').get()
                if tag_name == 'a':
                    link_text_parts = sub_node.xpath('.//text()').getall()
                    link_text = ' '.join(part.strip() for part in link_text_parts if part.strip()).strip()
                    link_href = sub_node.xpath('./@href').get()
                    
                    if link_href:
                        full_link_href = response.urljoin(link_href)
                        if link_text:
                            parts.append(f"{link_text} ({full_link_href})")
                        else:
                            parts.append(f"({full_link_href})")
                        
                        if full_link_href not in self.seen_links:
                            self.seen_links.add(full_link_href)
                            f_links.write(full_link_href + "\n")
                else:
                    element_text_parts = sub_node.xpath('.//text()').getall()
                    element_text = ' '.join(part.strip() for part in element_text_parts if part.strip()).strip()
                    if element_text:
                        parts.append(remove_tags(element_text))
            else:
                # This is a text node
                text_content = sub_node.get().strip()
                if text_content:
                    parts.append(remove_tags(text_content))
        
        return ' '.join(parts).strip()