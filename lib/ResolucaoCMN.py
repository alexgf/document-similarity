from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from lib.TextUtils import text_from_pdf

from lib.PageNotFoundException import PageNotFoundException

class ResolucaoCMN:
    def __init__(self, url = ''):
        self.url = url

    def load(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-infobars')
        self.driver = webdriver.Chrome('chromedriver', options=chrome_options)

        try:
            self.driver.get(self.url)
            wait = WebDriverWait(self.driver, 100)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.MsoNormal, ul.list-group.list-group-horizontal-sm.mb-3>li:last-child>a')))
        except TimeoutException:
            raise PageNotFoundException(self.url)
        else:
            html = self.driver.page_source
        finally:
            self.driver.quit()

        if html:
            return html
        else:
            raise PageNotFoundException(self.url)
            
    def get_text(self, html):
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('h2', 'titulo-pagina').get_text().strip().replace("\n", "")

        content=''
        if (soup.find('p', 'MsoNormal')):
            content_root = soup.find('p', 'MsoNormal').parent    
            spans = content_root.find_all('span')
            content = ' '.join(map(lambda x: x.get_text(), spans))
        elif (soup.select('ul.list-group.list-group-horizontal-sm.mb-3>li:last-child>a')):
            link = soup.select('ul.list-group.list-group-horizontal-sm.mb-3>li:last-child>a')[0]
            self.link = link['href']
            content = text_from_pdf(link['href'])

        return dict(
            title=title,
            text=content
        )
