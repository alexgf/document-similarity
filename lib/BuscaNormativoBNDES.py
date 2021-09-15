from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

from lib.PageNotFoundException import PageNotFoundException

class BuscaNormativoBNDES:
    def __init__(self):        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome('chromedriver', options=chrome_options)
        self.url = 'https://www.bndes.gov.br/wps/portal/site/home/instituicoes-financeiras-credenciadas/normas/normas-operacoes-indiretas'

    def load(self):
        try:
            self.driver.get(self.url)
            self.wait = WebDriverWait(self.driver, 100)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr>td>a.titulo')))
        except TimeoutException:
            raise PageNotFoundException(self.url)
        else:
            self.html = self.driver.page_source

        if self.html:
            return self.html
        else:
            raise PageNotFoundException(self.url)

    def get_results(self):
        links = self.driver.find_elements_by_css_selector('tr>td>a.titulo')
        if links != None and len(links) > 0:
            return list(map(lambda a: dict(title=a.get_attribute('innerHTML'), url=a.get_attribute('href')), links))
        return []

    def has_next_result_page(self):
        return True if 'disabled' not in self.__botao_proximo().get_attribute('class').split() else False
    
    def next_result_page(self):
        status_paginacao = self.driver.find_element_by_id('normas_info').get_attribute('innerHTML')
        link_proximo = self.__botao_proximo()
        self.driver.execute_script("arguments[0].click();", link_proximo)
        wait = WebDriverWait(self.driver, 100)
        wait.until(lambda driver: driver.find_element_by_id('normas_info').get_attribute('innerHTML') != status_paginacao)

    def __botao_proximo(self):
        return self.driver.find_element_by_id('normas_next')

    def close(self):
        self.driver.quit()