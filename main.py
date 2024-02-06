import os
import sys
import math
from bs4 import BeautifulSoup
from scraper import HomegateScraper
from gui import RealEstateApp
from db_admin import DBAdmin


def save_html_to_file(folder_name, file_name, html_content):
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


if __name__ == "__main__":
    db_admin = DBAdmin()
    app = RealEstateApp()
    app.root.mainloop()
    response = None
    scraper = HomegateScraper()
    args = app.args
    response, updated_url = scraper.run(args)

    if response:
        if response.status_code == 200:
            main_pages = []
            if not os.path.exists('HTML_Content'):
                os.makedirs('HTML_Content')
            save_html_to_file('HTML_Content',
                              f"{args["Type"]}-{args["City"]}-1",
                              response.text)

            soup = BeautifulSoup(response.text, 'html.parser')
            h1_tag = soup.find('h1', class_='ResultListHeader_locations_zQj9c')
            main_pages.append(updated_url)

            if h1_tag:
                total_ad_count = h1_tag.text.strip().split(' ')[0]
                print(" ".join(h1_tag.text.strip().split(' ')[:2]) + " found")
            else:
                print("Number of results is not found.")
                sys.exit(1)

            ad_tags = soup.find_all('a', class_=("HgCardElevated_content_uir_2"
                                                 " HgCardElevated_link_EHfr7"))
            scraper.parse(ad_tags, args)

            if ad_tags:
                ad_links = ["https://www.homegate.ch" + ad.get('href')
                            for ad in ad_tags]
                page_count = math.ceil(int(total_ad_count) / len(ad_links))
            else:
                print("The URLs for the ads are not found.")
                sys.exit(1)

            if page_count > 1:
                for page in range(2, page_count + 1):
                    page_url = updated_url + f"ep={page}"
                    res = scraper.fetch(page_url)
                    if res:
                        if response.status_code == 200:
                            save_html_to_file('HTML_Content',
                                              f"{args["Type"]}-{args["City"]}"
                                              f"-{page}",
                                              res.text)
                            soup = BeautifulSoup(res.text, 'html.parser')
                            class_ad_tags = ("HgCardElevated_content_uir_2"
                                             " HgCardElevated_link_EHfr7")
                            ad_tags = soup.find_all('a', class_=class_ad_tags)
                            scraper.parse(ad_tags, args)
                            main_pages.append(page_url)
                            for ad in ad_tags:
                                ad_links.append("https://www.homegate.ch" +
                                                ad.get('href'))

    if scraper.results:
        db_admin.add_info(scraper.results)
        print("The info is saved to MongoDB.")
