from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

from lib.PageNotFoundException import PageNotFoundException

class BuscaNormativoBacen:
    def __init__(self):        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-infobars')
        self.driver = webdriver.Chrome('chromedriver', options=chrome_options)
        self.url = 'https://www.bcb.gov.br/estabilidadefinanceira/buscanormas'
        
    def load(self):
        try:
            self.driver.get(self.url)
            self.wait = WebDriverWait(self.driver, 100)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-primary')))
        except TimeoutException:
            raise PageNotFoundException(self.url)
        else:
            self.html = self.driver.page_source

        if self.html:
            return self.html
        else:
            raise PageNotFoundException(self.url)
    
    def pesquisar(self, data_inicio, data_fim, tipo_documento='Resolução CMN'):
        self.__set_tipo_documento(tipo_documento)
        self.__set_data_inicio(data_inicio)
        self.__set_data_fim(data_fim)
        self.__pesquisar()
        self.url = self.driver.current_url
        
    def has_next_result_page(self):
        botao = self.__botao_proximo()
        if not botao:
            return False
        return True if 'disabled' not in self.__botao_proximo().get_attribute('class').split() else False
    
    def next_result_page(self):
        primeiro_resultado = self.driver.find_element_by_css_selector('li:first-child.resultado-item>a').get_attribute('href')
        link_proximo = self.__botao_proximo().find_element_by_tag_name('a')
        self.driver.execute_script("arguments[0].click();", link_proximo)
        wait = WebDriverWait(self.driver, 100)
        wait.until(lambda driver: driver.find_element_by_css_selector('li:first-child.resultado-item>a').get_attribute('href') != primeiro_resultado)
        
        self.url = self.driver.current_url
        
    def get_results(self):
        links = self.driver.find_elements_by_css_selector('li.resultado-item>a')
        if links != None and len(links) > 0:
            return list(map(lambda a: a.get_attribute('href'), links))
        return []

    def close(self):
        self.driver.quit()
        
    def back(self):
        self.driver.execute_script("window.history.go(-1)")

    def resolucao_source(self, href):
        self.driver.get(href)
        wait = WebDriverWait(self.driver, 100)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.MsoNormal, ul.list-group.list-group-horizontal-sm.mb-3>li:last-child>a')))

        return self.driver.page_source
    
    def __botao_proximo(self):
        elements =  self.driver.find_elements_by_css_selector('ul.pagination>li.page-item:nth-last-child(2)')
        if elements :
            return elements[0]
        return None
        
    def __pesquisar(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_css_selector('button.btn.btn-primary').click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3')))
        
    def __set_data_inicio(self, data_inicio):
        input_data_inicio = self.driver.find_element_by_id('dataInicioBusca')
        input_data_inicio.clear()
        input_data_inicio.send_keys(data_inicio)
        
    def __set_data_fim(self, data_fim):
        input_data_fim = self.driver.find_element_by_id('dataFimBusca')
        input_data_fim.clear()
        input_data_fim.send_keys(data_fim)
        
    def __set_tipo_documento(self, tipo_documento):
        select_tipo_documento = Select(self.driver.find_element_by_id('tipoDocumento'))
        select_tipo_documento.select_by_value(tipo_documento)