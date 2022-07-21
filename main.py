from src.config import EXCEL_HEADER_LIST
from src.excel_writer import create_excel
from src.utils import get_driver_beta, scrap

if __name__ == '__main__':
    driver = get_driver_beta()
    create_excel('SlowHopeLastMinutesSelenium', 'Last_minute', EXCEL_HEADER_LIST, scrap(driver))
    driver.quit()
