import datetime
import time

from s3p_sdk.exceptions.parser import S3PPluginParserOutOfRestrictionException, S3PPluginParserFinish
from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from s3p_sdk.types import S3PRefer, S3PDocument, S3PPlugin
from s3p_sdk.types.plugin_restrictions import FROM_DATE, S3PPluginRestrictions
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import dateparser
from random import uniform

class MIT(S3PParserBase):
    """
    A Parser payload that uses S3P Parser base class.
    """

    def __init__(self, refer: S3PRefer, plugin: S3PPlugin, web_driver: WebDriver, restrictions: S3PPluginRestrictions):
        super().__init__(refer, plugin, restrictions)

        # Тут должны быть инициализированы свойства, характерные для этого парсера. Например: WebDriver
        self._driver = web_driver
        self._wait = WebDriverWait(self._driver, timeout=20)

    def _parse(self):
        """
        Метод, занимающийся парсингом. Он добавляет в _content_document документы, которые получилось обработать
        :return:
        :rtype:
        """
        # HOST - это главная ссылка на источник, по которому будет "бегать" парсер
        self.logger.debug(F"Parser enter")

        # ========================================
        # Тут должен находится блок кода, отвечающий за парсинг конкретного источника
        # -

        topics = {'Social media': 'https://news.mit.edu/topic/social-media',
                  'Wearable sensors': 'https://news.mit.edu/topic/wearable-sensors',
                  'Data': 'https://news.mit.edu/topic/data',
                  'School of Engineering': 'https://news.mit.edu/topic/school-engineering',
                  'Wearables': 'https://news.mit.edu/topic/wearables',
                  'Web': 'https://news.mit.edu/topic/web',
                  'Web development': 'https://news.mit.edu/topic/web-development',
                  'Social networks': 'https://news.mit.edu/topic/social-networks',
                  'Sustainability': 'https://news.mit.edu/topic/sustainability',
                  'System Design and Management': 'https://news.mit.edu/topic/system-design-and-management',
                  'Systems design': 'https://news.mit.edu/topic/systems-design',
                  'Systems engineering': 'https://news.mit.edu/topic/systems-engineering',
                  'Taxes': 'https://news.mit.edu/topic/taxes',
                  'Technology': 'https://news.mit.edu/topic/technology',
                  'Technology and policy': 'https://news.mit.edu/topic/technology-and-policy',
                  'Technology and society': 'https://news.mit.edu/topic/technology-society',
                  'Information systems and technology': 'https://news.mit.edu/topic/information-systems-and-technology',
                  'Information theory': 'https://news.mit.edu/topic/information-theory',
                  'Innovation and Entrepreneurship (I&E)': 'https://news.mit.edu/topic/innovation',
                  'Internet': 'https://news.mit.edu/topic/internet',
                  'Internet of things': 'https://news.mit.edu/topic/internet-things',
                  'Internet privacy': 'https://news.mit.edu/topic/internet-privacy',
                  'Machine learning': 'https://news.mit.edu/topic/machine-learning',
                  'Marketing': 'https://news.mit.edu/topic/marketing',
                  'Natural language processing': 'https://news.mit.edu/topic/natural-language-processing',
                  'Programming': 'https://news.mit.edu/topic/programming',
                  'Programming languages': 'https://news.mit.edu/topic/programming-languages',
                  'Quantum mechanics': 'https://news.mit.edu/topic/quantum-mechanics',
                  'Quantum computing': 'https://news.mit.edu/topic/quantum-computing',
                  'Quantum dots': 'https://news.mit.edu/topic/quantumdots',
                  'smartphones': 'https://news.mit.edu/topic/smartphones',
                  'Global economic crisis': 'https://news.mit.edu/topic/global-economic-crisis',
                  'Global economy': 'https://news.mit.edu/topic/global-economy',
                  'Google': 'https://news.mit.edu/topic/google',
                  'Facebook': 'https://news.mit.edu/topic/facebook',
                  'Finance': 'https://news.mit.edu/topic/finance',
                  'finances': 'https://news.mit.edu/topic/finances',
                  'Financial aid': 'https://news.mit.edu/topic/financial-aid',
                  'Electrical engineering and electronics': 'https://news.mit.edu/topic/electrical-engineering',
                  'Electrical engineering and computer science (EECS)': 'https://news.mit.edu/topic/electrical-engineering-and-computer-science-eecs',
                  'Electrical Engineering & Computer Science (eecs)': 'https://news.mit.edu/topic/electrical-engineering-computer-science-eecs',
                  'Cryptography': 'https://news.mit.edu/topic/cryptography',
                  'Cybersecurity': 'https://news.mit.edu/topic/cyber-security',
                  'Computer science and technology': 'https://news.mit.edu/topic/computers',
                  'Computer vision': 'https://news.mit.edu/topic/computer-vision',
                  'Analytics': 'https://news.mit.edu/topic/analytics',
                  'Artificial intelligence': 'https://news.mit.edu/topic/artificial-intelligence2',
                  'Big data': 'https://news.mit.edu/topic/big-data',
                  'Blockchain': 'https://news.mit.edu/topic/blockchain'}

        # chrome_options = webdriver.ChromeOptions()
        """Объект опций запуска драйвера браузера Chrome"""

        # chrome_options.add_argument('--headless')
        """Опция Chrome - Запуск браузера без пользовательского интерфейса (в фоне)"""

        for i, topic in enumerate(topics):
            try:
                self._driver.get(topics[topic])
                self._wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.page-term--views--list')))
            except:
                # print(f'=== Не удалось загрузить ({i + 1}/{len(topics)}) {topic} ===\nПропуск...')
                continue
            # print(f'=== ({i + 1}/{len(topics)}) {topic} ===')
            more_pages = True
            while more_pages:
                try:
                    el_list = self._driver.find_elements(By.TAG_NAME, 'article')
                except Exception as e:
                    el_list = []
                    # print('Error finding articles')
                for j, el in enumerate(el_list):
                    title = el_list[j].find_element(By.CLASS_NAME, 'term-page--news-article--item--title--link').text
                    web_link = el_list[j].find_element(By.CLASS_NAME,
                                                       'term-page--news-article--item--title--link').get_attribute(
                        'href')

                    try:
                        abstract = el_list[j].find_element(By.CLASS_NAME, 'term-page--news-article--item--dek').text
                    except:
                        # print('No abstract')
                        abstract = ''

                    pub_date = dateparser.parse(el_list[j].find_element(By.TAG_NAME, 'time').get_attribute('datetime'))
                    pub_date = pub_date.replace(tzinfo=None)
                    self._driver.execute_script("window.open('');")
                    self._driver.switch_to.window(self._driver.window_handles[1])
                    try:
                        self._driver.get(web_link)
                        self._wait.until(
                            ec.presence_of_element_located((By.CSS_SELECTOR, '.news-article--content--body--inner')))
                        # time.sleep(uniform(0.5, 1.5))
                    except Exception as e:

                        self._driver.close()
                        self._driver.switch_to.window(self._driver.window_handles[0])
                        continue
                    text_content = self._driver.find_element(By.CLASS_NAME, 'news-article--content--body--inner').text
                    try:
                        related_topics = [x.text for x in self._driver.find_elements(By.XPATH,
                                                                                     '//li[@class=\'news-article--topics-list--item\']')]
                    except:
                        related_topics = ''
                    try:
                        author = self._driver.find_element(By.CLASS_NAME, 'news-article--authored-by').text
                    except:
                        author = ''
                    other_data = {}
                    other_data['tags'] = related_topics
                    other_data['author'] = author

                    doc = S3PDocument(id=None,
                                      title=title,
                                      abstract=abstract,
                                      text=text_content,
                                      link=web_link,
                                      storage=None,
                                      other=other_data,
                                      published=pub_date,
                                      loaded=datetime.datetime.now())

                    try:
                        self._find(doc)
                    except S3PPluginParserOutOfRestrictionException as e:
                        if e.restriction == FROM_DATE:
                            self.logger.debug(f'Document is out of date range `{self._restriction.from_date}`')
                            raise S3PPluginParserFinish(self._plugin,
                                                        f'Document is out of date range `{self._restriction.from_date}`',
                                                        e)

                    self._driver.close()
                    self._driver.switch_to.window(self._driver.window_handles[0])

                try:
                    next_page = self._driver.find_element(By.XPATH, '//*[contains(@class, \'pager--button--next\')]')

                    self._driver.execute_script('arguments[0].click()', next_page)
                    time.sleep(uniform(0.5, 1.5))

                    more_pages = True
                except Exception as e:

                    more_pages = False

        # ---
        # ========================================
        ...
