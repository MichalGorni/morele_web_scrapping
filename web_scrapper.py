import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import date


BASER_DIR = os.path.dirname(__file__)


class MoreleScrapper:
    """
    Connects with Morele.net online shop and gets smartphone offers
    """

    def __init__(self) -> None:
        self.url = r"https://www.morele.net/kategoria/smartfony-280/"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def get_pages(self, max_pages: int | None = None) -> None:
        container = self.soup.find("div", {"class": "pagination-wrapper"})
        last_page = container.find(
            "div", {"class": "pagination-btn-nolink-anchor"}
        ).text.strip()
        last_page = int(last_page)
        print(f"Total pages: {last_page}")
        if max_pages is not None and last_page > max_pages:
            print(f"Pagination limited by user to: {max_pages}")
            last_page = max_pages
        return last_page

    def get_offers_from_page(self, page) -> list:
        """
        Gets offers from a singe page
        """
        url = rf"https://www.morele.net/kategoria/smartfony-280/,,,,,,,,0,,,,/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        panel = soup.find("div", {"class": "category-list"})
        container = panel.find("div", {"class": "cat-list-products"})
        offers = container.find_all("div", {"class": "cat-product card"})
        names = []
        prices = []
        links = []
        for offer in offers:
            name = offer.find("h2", {"class": "cat-product-name__header"})
            price = offer.find("div", {"class": "price-new"})
            link = offer.find("a", {"class": "productLink"})["href"]
            if name is not None:
                name = name.text.strip()
            else:
                name = "Name not found"
            if price is not None:
                price = price.text.strip()
            else:
                price = "Price not found"
            if link is not None:
                link = f"https://www.morele.net{link}"
            else:
                link = "Link not found"

            names.append(name)
            prices.append(price)
            links.append(link)

            print(f"Name:{name}")
            print(f"Price: {price}")
            print(f"Link: {link}")

        return names, prices, links

    def scrap_website(self, max_pages: int | None = None) -> dict[str, str | int]:
        """
        Iterates over multiple pages and gets offers from eachs
        """
        names = []
        prices = []
        links = []
        pages = self.get_pages(max_pages)
        for page in range(1, pages + 1):
            print(f"Scrapping page {page} out of {pages}")
            pg_names, pg_prices, pg_links = self.get_offers_from_page(page)
            names.extend(pg_names)
            prices.extend(pg_prices)
            links.extend(pg_links)
        data = {"Name": names, "Price": prices, "Link": links}
        return data
