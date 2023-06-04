import webbrowser
import argparse
from tqdm import tqdm

from parserFlatIds import PageParser
from flatPageParser import FlatParser
from csvCreator import CSVMaker


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_link", default="https://www.cian.ru/cat.php?deal_type=sale&engine_version=2"\
                        "&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1", type=str)
    parser.add_argument("--start_page", default=1, type=int)
    parser.add_argument("--output", default="./data.csv", type=str)
    return parser


if __name__ == "__main__":
    parser = argument_parser().parse_args()

    IDParser = PageParser(base_link=parser.base_link, start_page_index=parser.start_page)
    IDs = IDParser.get_ids()

    FParser = FlatParser()
    flat_description = {}

    for flat_id in tqdm(IDs, "Iterating through flats..."):
        price, rooms, underground, main, general, house = FParser.parse_page(flat_id)
        flat_data = []
        flat_data.append(("price", price))
        flat_data.append(("rooms", rooms))
        flat_data.append(("sub", underground[0] + underground[1]))
        for main_key in main.keys():
            flat_data.append((main_key, main[main_key]))
        for general_key in general.keys():
            flat_data.append((general_key, general[general_key]))
        for house_key in house.keys():
            flat_data.append((house_key, house[house_key]))
        flat_description[flat_id] = flat_data

    CSV = CSVMaker(categories=FParser.get_categories(), data=flat_description, output=parser.output)
    CSV.get_csv()
