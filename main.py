import os

from web_scrapper import MoreleScrapper
from data_transformation import DataTransformations


def get_offers() -> None:
    """
    Main function aggregating script flow
    Allows user to choose how many pages will be scrapped
    """

    page_limit = 0
    while page_limit <= 0:
        page_limit = input(
            "How many pages do you want to scrapp?\nPress enter to scrap all available pages:\n"
        )
        try:
            page_limit = int(page_limit)
            if page_limit > 0:
                break
            else:
                print("Value must be bigger than 0")
        except ValueError or TypeError:
            print("Value must be an integer bigger than 0")
            page_limit = 0

    scrapper = MoreleScrapper()
    data = scrapper.scrap_website(page_limit)
    transformator = DataTransformations(data)
    transformator.save_data()
    os.startfile(transformator.file_path)


if __name__ == "__main__":
    get_offers()
