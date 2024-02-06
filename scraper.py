import re
import requests


class HomegateScraper:
    def __init__(self):
        self.results = []
        self.base_url = ("https://www.homegate.ch/{ad_type}/{category}"
                         "/city-{city}/matching-list?{km}{room}{price}")

    def generate_urls(self, args):
        return self.base_url.format(ad_type=args["Type"].lower(),
                                    category=args["Category"].lower(),
                                    city=args["City"].lower(),
                                    km="be=" + str(float(
                                        args["Kilometer"]
                                        )*1000)
                                    if args["Kilometer"] != "0" else '',
                                    room="&ac=" + str(args["Rooms"])
                                    if args["Rooms"] else '',
                                    price="&ah=" + str(args["Price"]) if
                                    args["Price"] != "any" else '').strip()

    def fetch(self, url):
        print(f'HTTP GET request to URL: {url}')
        try:
            res = requests.get(url)
            print(f'Status Code: {res.status_code} | Reason: {res.reason}')

        except requests.RequestException as e:
            print(f"Error during the request: {e}")

        else:
            return res

    def parse(self, a_tags, args):
        for a_tag in a_tags:
            info = {}
            info["Ad Type"] = args["Type"]
            pictures = []
            picture_tags = a_tag.find_all('picture')
            for picture_tag in picture_tags:
                source_tag = picture_tag.find('source')
                if source_tag:
                    srcset = source_tag.get('srcset', '')
                    src_urls = [url.strip().split(' ')[0]
                                for url in srcset.split(',')]
                    pictures = pictures + src_urls
                else:
                    img_tag = picture_tag.find('img')
                    if img_tag:
                        img_src = img_tag.get('src', '')
                        pictures.append(img_src)
            info["Picture"] = (list(set(picture for picture in pictures
                                        if picture.find("1092x") != -1))
                               if pictures else 'N/A')
            address = a_tag.find('address')
            if address:
                info['Address'] = address.text.strip()
            else:
                info['Address'] = 'N/A'

            div_tag = a_tag.find('div', class_='HgListingCard_mainTitle_x0p2D')
            if div_tag:
                span_tag = div_tag.find('span',
                                        class_='HgListingCard_price_JoPAs')
                if span_tag:
                    price = span_tag.text.strip()
                    if price != 'Price on request':
                        info['Price'] = price.split(' ')[1].split('.')[0]
                    elif price == 'Price on request':
                        info['Price'] = 'Price on request'
                    else:
                        info['Price'] = 'N/A'

            # Find a div with the specified class
            div = a_tag.find('div',
                             class_=("HgListingRoomsLivingSpace_"
                                     "roomsLivingSpace_GyVgq"))

            spans = div.find_all('span')

            if not spans:
                info['Room'] = 'N/A'
                info['Space'] = 'N/A'
            else:
                # Use regular expressions to extract all numbers
                for span in spans:
                    text_content = span.get_text().strip()

                    match_r = re.search(".*rooms$", text_content)
                    match_s = re.search(".*living space$", text_content)

                    if match_r:
                        info['Room'] = match_r[0].split(' ')[0]

                    if match_s:
                        info['Space'] = (match_s[0].split(' ')[0]
                                         .replace('m²', ''))

                if 'Room' not in info:
                    info['Room'] = 'N/A'

                if 'Space' not in info:
                    info['Space'] = 'N/A'

            ps = a_tag.find('p', class_='HgListingDescription_title_NAAxy')
            if ps:
                title = ps.find('span')
                if title:
                    info['Title'] = title.text.strip()
            else:
                info['Title'] = 'N/A'

            ps = a_tag.find('div', class_=("HgListingDescription_"
                                           "description_r5HCO"
                                           " HgListingCard_description_kmLhw"))
            description_large = ps.find('p', class_=("HgListingDescription_"
                                                     "large_uKs3J"))
            description_medium = ps.find('p', class_=("HgListingDescription_"
                                                      "medium_NzKMY"))
            description_small = ps.find('p', class_=("HgListingDescription_"
                                                     "small_Q7_Og"))
            if description_large:
                info['Description'] = description_large.text.strip()
            elif description_small:
                info['Description'] = description_small.text.strip()
            elif description_medium:
                info['Description'] = description_medium.text.strip()
            else:
                info['Description'] = 'N/A'

            self.results.append(info)

    def run(self, user_args):
        updated_url = self.generate_urls(user_args)
        res = self.fetch(updated_url)
        return res, updated_url
