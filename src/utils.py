from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.config import PATH, WEBSITE, MONTHS_TO_NUMBERS, DAY_NUMS_TO_DAYS, BASE_WEBSITE, PATH_BETA, YEAR, MONTH


def get_driver():
    """ creates selenium driver"""
    # path is set to beta version (104) of chrome since current stable version (103) is bugged.
    # if chrome version 104 is out update chrome and change path to stable version

    service = Service(executable_path=PATH_BETA)
    options = webdriver.ChromeOptions()
    options.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_pages_quantity(driver) -> int:
    return int(driver.find_element(By.XPATH,
                                   '//*[@id="content-wrapper"]/div/div/div/div/div[3]/div/section/div[3]/div[7]/a').text)


def get_offers(driver) -> list:
    return driver.find_elements(By.CLASS_NAME, 'catalog-tile')


def get_description(offer) -> dict[str]:
    description = offer.find_element(By.CLASS_NAME, 'catalog-tile__si-name').text
    return {'opis': description}


def get_place(offer) -> dict[str]:
    place_raw = offer.find_element(By.CLASS_NAME, 'catalog-tile__location').text.split(',')
    place = place_raw[1]
    country = place_raw[0]
    return {'miejsce': place, 'kraj': country}


def get_url(offer) -> dict[str]:
    link = offer.find_element(By.XPATH, './a[@class="catalog-tile__link"]').get_attribute('href')
    return {'strona': link}


def get_location_name(offer) -> dict[str]:
    location_name = offer.find_element(By.CLASS_NAME, 'catalog-tile__name').text
    return {'nazwa': location_name}


def weekday(date) -> str:
    """ creates str of weekday in polish """
    return DAY_NUMS_TO_DAYS.get(datetime.strptime(date, '%d.%m.%Y').weekday())


def get_dates_and_size(offer) -> dict:
    """ gets dates from offer as well as information on how many people is it for
        unfolds string with dates from html, splits it to day and month. Since year is not given adds it from datetime
        accordingly to offer dates.
        week_day_in and out returns weekdays in polish
        stay lengh and size is returned as ints"""

    raw_dates = offer.find_element(By.CLASS_NAME, 'catalog-tile__period-details').text.split()
    day_in = raw_dates[0]
    day_out = raw_dates[3]
    month_in_raw = MONTHS_TO_NUMBERS.get(raw_dates[1])
    month_out_raw = MONTHS_TO_NUMBERS.get(raw_dates[4])
    month_in = str('0' + str(month_in_raw)) if month_in_raw < 10 else str(month_in_raw)
    month_out = str('0' + str(month_out_raw)) if month_out_raw < 10 else str(month_out_raw)
    year_in = str(YEAR) if not month_in_raw < MONTH else str(YEAR + 1)
    year_out = str(YEAR) if not month_out_raw < MONTH else str(YEAR + 1)
    date_in = day_in + '.' + month_in + '.' + year_in
    date_out = day_out + '.' + month_out + '.' + year_out
    week_day_in = weekday(date_in)
    week_day_out = weekday(date_out)
    lengh = week_day_in + ' - ' + week_day_out
    stay_lengh = int(raw_dates[5].replace('(', ''))
    size = int(raw_dates[8])
    return {'od do': lengh, 'zameldowanie': date_in, 'wymeldowanie': date_out, 'długość pobytu (noce)': stay_lengh,
            'ilość osób': size}


def get_price(offer) -> dict:
    """returns new price, old price if accesible, savings and currency"""

    currency = offer.find_element(By.XPATH, './/div[2]/p[2]').text[-3:]
    old_price_raw = offer.find_element(By.XPATH, './/div[2]/p[1]').text[:-4].replace(' ', '')
    old_price = int(old_price_raw) if old_price_raw != '' else old_price_raw
    new_price = int(offer.find_element(By.XPATH, './/div[2]/p[2]').text[:-4].replace(' ', ''))
    savings = old_price - new_price if old_price != '' else '-'
    return {'nowa cena': new_price, 'stara cena': old_price, 'waluta': currency, 'oszczędność': savings}


def calculate_day_price(stay_lengh: int, price: int) -> int:
    return round(price / stay_lengh)


def get_data(offer) -> list[dict]:
    """ executes all the functions that get data from the site
        calculates prices per person and per day"""

    name = get_location_name(offer)
    description = get_description(offer)
    dates = get_dates_and_size(offer)
    price = get_price(offer)
    place = get_place(offer)
    url = get_url(offer)
    size = dates.get('ilość osób')
    new_price = price.get('nowa cena')
    stay_lengh = dates.get('długość pobytu (noce)')
    per_day = round(new_price / stay_lengh)
    per_person = round(new_price / size)
    per_person_per_day = round(per_person / stay_lengh)
    price_per_person = {'za osobę': per_person}
    price_per_day = {'cena za dzień': per_day}
    price_per_person_per_day = {'za osobę za dzień': per_person_per_day}

    return [place, name, description, price, price_per_day, price_per_person, price_per_person_per_day, dates, url]


def dictify(data) -> dict:
    """takes list of dicts with offers and returns it as one dict"""

    offers = {}
    for offer in data:
        offers.update(offer)
    return offers


def set_wait(driver, wait_time: int, element_name: str):
    """returns condition that must be fulfilled to continue iteration with wait time"""

    wait = WebDriverWait(driver, wait_time)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, element_name)))
    return element


def scrap(driver) -> list[dict]:
    """ takes driver from get_driver() as argument and connects to slowhop.com via chrome.
        page_quantity checks number of pages to iterate.
        every iteration is executed after the 'tiles' element has been found.

        returns a list of offers sorted by check-in date """

    scraped = []
    driver.get(BASE_WEBSITE)
    pages_quantity = get_pages_quantity(driver)
    for page in range(1, pages_quantity + 1):
        driver.get(WEBSITE.format(page=page))
        wait = WebDriverWait(driver, 10)
        tiles = set_wait(wait, 10, 'grid-results__tiles')
        offers = get_offers(tiles)
        for offer in offers:
            try:
                scraped.append(dictify(get_data(offer)))
            except Exception as e:
                print(e)

    return sorted(scraped, key=lambda d: datetime.strptime(d['zameldowanie'], '%d.%m.%Y'))
