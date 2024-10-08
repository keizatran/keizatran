import logging
import argparse
from dotenv import load_dotenv

from . import scraper

if __name__ == "__main__":

    load_dotenv()

    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(dest="module")

    scraper_parser = sub_parser.add_parser("scraper")

    scraper_parser.add_argument(
        "-p",
        "--page",
        dest="scraper_page",
        type=int,
        help="starting page search all products",
    )

    scraper_parser.add_argument(
        "-ur",
        "--unraw",
        dest="scraper_unraw",
        action="store_true",
        help="scrap raw data",
    )

    scraper_parser.add_argument(
        "-ps",
        "--parsed",
        dest="scraper_parsed",
        action="store_true",
        help="parse raw data",
    )

    args = parser.parse_args()

    if args.module == "scraper":
        logging.basicConfig(
            filename="log/pharmacy.scraper.log",
            filemode="a",
            format="%(asctime)s [%(levelname)s]: %(message)s",
            level=logging.INFO,
        )
        if args.scraper_page is not None:
            scraper.search_products(page=args.scraper_page)
        elif args.scraper_unraw:
            scraper.get_product()
        elif args.scraper_parsed:
            scraper.parse_product()
