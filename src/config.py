from datetime import datetime

YEAR = datetime.now().year
MONTH = datetime.now().month

PATH = "/Users/tszos/Documents/browser_drivers/chromedriver"
PATH_BETA = "/Users/tszos/Documents/browser_drivers/beta/chromedriver"

BASE_WEBSITE = 'https://slowhop.com/pl/last-minute'
WEBSITE = "https://slowhop.com/pl/last-minute?page={page}"

MONTHS_TO_NUMBERS = {'sty': 1, 'lu': 2, 'mar': 3,
                     'kwi': 4, 'maj': 5, 'cze': 6,
                     'lip': 7, 'sie': 8, 'wrz': 9,
                     'paź': 10, 'lis': 11, 'gru': 12}

DAY_NUMS_TO_DAYS = {1: 'poniedziałek', 2: 'wtorek', 3: 'środa', 4: 'czwartek', 5: 'piątek', 6: 'sobota', 0: 'niedziela'}

EXCEL_HEADER_LIST = ['miejsce', 'kraj', 'nazwa', 'opis', 'ilość osób', 'nowa cena', 'stara cena', 'cena za dzień',
                     'za osobę', 'za osobę za dzień', 'waluta', 'oszczędność', 'od do', 'zameldowanie',
                     'wymeldowanie', 'długość pobytu (noce)', 'strona']