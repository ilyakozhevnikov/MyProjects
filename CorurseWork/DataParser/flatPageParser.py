from bs4 import BeautifulSoup
from selenium import webdriver


class FlatParser:
    def __init__(self, base_url="https://www.cian.ru/sale/flat/"):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(executable_path="chromedriver", options=self.options)
        self.base_url = base_url
        self.categories = set()

    def __get_page_data__(self, driver, url):
        driver.get(url)
        return BeautifulSoup(driver.page_source, "html.parser")

    def __price__(self, content):
        side_card = content.find("div", attrs={"data-name": "OfferCardAside"})
        if side_card is None:
            return ""
        price_span = side_card.find("span", attrs={"itemprop": "price"})["content"]
        return price_span

    def __rooms__(self, content):
        front_card = content.find("div", attrs={"data-name": "OfferTitle"})
        if front_card is None:
            return ""
        return front_card.find("h1").contents[0].split(',')[0]

    def __subway__(self, content):
        geo = content.find("div", attrs={"data-name": "Geo"})
        if geo is None:
            return ""
        station, time = "", ""
        for element in geo.find_all(class_=True):
            for value in element["class"]:
                if "underground_link" in value:
                    station = geo.find("a", attrs={"class": value}).contents[0]
                if "underground_time" in value:
                    time = geo.find("span", attrs={"class": value}).contents[-1]
            if station != "" and time != "":
                return station, time
        return station, time

    def __main_section__(self, content):
        summary = content.find("div", attrs={"data-name": "ObjectSummaryDescription"})
        if summary is None:
            return {}
        data = {}
        for datapoint in summary.find_all("div", attrs={"data-testid": "object-summary-description-info"}):
            value = datapoint.find("div", attrs={"data-testid": "object-summary-description-value"}).contents[0]
            title = datapoint.find("div", attrs={"data-testid": "object-summary-description-title"}).contents[0]
            data[title] = value
        self.categories.update(data.keys())
        return data

    def __general_section__(self, content):
        general = content.find("div", attrs={"data-name": "GeneralInformation"})
        if general is None:
            return {}
        data = {}
        for datapoint in general.find_all("li", attrs={"data-name": "AdditionalFeatureItem"}):
            flag = False
            title, value = None, None
            for elem in datapoint:
                if not flag:
                    title = elem.contents[0]
                    flag = True
                else:
                    value = elem.contents[0]
            data[title] = value
        self.categories.update(data.keys())
        return data

    def __house_info__(self, content):
        house_data = content.find("div", attrs={"data-name": "BtiContainer"})
        if house_data is None:
            return {}
        data = {}
        for datapoint in house_data.find_all("div", attrs={"data-name": "Item"}):
            flag = False
            title, value = None, None
            for elem in datapoint:
                if not flag:
                    title = elem.contents[0]
                    flag = True
                else:
                    value = elem.contents[0]
            data[title] = value
        self.categories.update(data.keys())
        return data

    def parse_page(self, flat_id):
        url = self.base_url + str(flat_id) + "/"
        content = self.__get_page_data__(self.driver, url)
        price = self.__price__(content)
        rooms = self.__rooms__(content)
        underground = self.__subway__(content)
        main_data = self.__main_section__(content)
        general_data = self.__general_section__(content)
        house_info = self.__house_info__(content)
        return price, rooms, underground, main_data, general_data, house_info

    def get_categories(self):
        self.categories.add("sub")
        self.categories.add("price")
        self.categories.add("id")
        return self.categories
