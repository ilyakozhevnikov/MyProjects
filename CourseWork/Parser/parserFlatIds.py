from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re


class PageParser:
    def __init__(self, base_link, start_page_index=1):
        self.base_link = base_link
        self.page_index = start_page_index
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(executable_path="chromedriver", options=self.options)
        self.ids = []

    def __get_next_page__(self, bs4_object):
        """
        :param: bs4_object: bs4 object to parse it
        :return: int page: page index, None: if we are on the last page
        """
        page_bar = bs4_object.find("div", attrs={"data-name": "Pagination"}).find("ul").find_all("li")
        available_pages = []
        for x in page_bar:
            if x is not None:
                available_pages.append(int(re.findall("[0-9]+", string=str(x))[-1]))  # Getting the page number
        if self.page_index not in available_pages:
            return None
        if (self.page_index + 1) not in available_pages:
            return None
        return self.page_index + 1

    def __get_flat_ids__(self, bs4_object):
        """
        :param: bs4_object: bs4 object to parse it
        :return: python list with parsed ids of pages with flat advertisements
        """
        for flat_card in bs4_object.find_all("article", attrs={"data-name": "CardComponent"}):
            if flat_card is not None:
                link = flat_card.find("div", attrs={"data-name": "LinkArea"})
                if link is not None:
                    link = link.a['href']
                self.ids.append(int(link.split("/")[-2]))

    def __parse__(self):
        self.driver.get(self.base_link)
        # Waiting to get through CIAN.RU Checks
        time.sleep(10)
        # Все
        self.driver.get(self.base_link)
        initial_content = BeautifulSoup(self.driver.page_source, "html.parser")

        while self.page_index is not None:
            self.__get_flat_ids__(initial_content)
            self.page_index = self.__get_next_page__(initial_content)
            page_url = f"&p={self.page_index}"
            self.driver.get(self.base_link + page_url)
            initial_content = BeautifulSoup(self.driver.page_source, "html.parser")
        # TODO: Implement parsing "SHOW MORE" if have enough time

    def get_ids(self):
        self.__parse__()
        return self.ids
