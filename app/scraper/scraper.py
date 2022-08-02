import io
import time
import requests
from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class ImageScraper:

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.__get_default_chrome_options())
    def get_image_urls(self, query: str, max_urls: int, sleep_between_interactions: int = 1):
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
        self.driver.get(search_url.format(q=query))

        image_urls = set()
        image_count = 0
        results_start = 0
        while image_count < max_urls:
            self.__scroll_to_end(sleep_between_interactions)
            thumbnail_results = self.driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
            number_results = len(thumbnail_results)
            print("Found: {0} search results. Extracting links from {1}:{0}".format(number_results, results_start))

            for img in thumbnail_results[results_start:number_results]:
                self.__click_and_wait(img, sleep_between_interactions)
                self.__add_image_urls_to_set(image_urls)
                image_count = len(image_urls)
                if image_count >= max_urls:
                    print("Found: {} image links, done!".format(len(image_urls)))
                    break
            else:
                print("Found: {} image links, looking for more ...".format(len(image_urls)))

                load_more_button = self.driver.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    print("loading more...")
                    self.driver.execute_script("document.querySelector('.mye4qd').click();")

            # move the result startpoint further down
            results_start = len(thumbnail_results)

        return image_urls

    def get_in_memory_image(self, url: str, format: str):
        image_content = self.__download_image_content(url)
        try:
            image_file = io.BytesIO(image_content)
            pil_image = Image.open(image_file).convert('RGB')
            in_mem_file = io.BytesIO()
            pil_image.save(in_mem_file, format=format)
            
            return in_mem_file.getvalue()
        except Exception as e:
            print("Could not get image data: {}".format(e))

    def close_connection(self):
        self.driver.quit()

    def __download_image_content(self, url):
        try:
            return requests.get(url).content
        except Exception as e:
            print("ERROR - Could not download {} - {}".format(url, e))

    def __scroll_to_end(self, sleep_time):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time)

    def __click_and_wait(self, img, wait_time):
        try:
            img.click()
            time.sleep(wait_time)
        except Exception:
            return

    def __add_image_urls_to_set(self, image_urls: set):
        actual_images = self.driver.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
        for actual_image in actual_images:
            if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                image_urls.add(actual_image.get_attribute('src'))

    def __get_default_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # lambda_options = [
        #     '--autoplay-policy=user-gesture-required',
        #     '--disable-background-networking',
        #     '--disable-background-timer-throttling',
        #     '--disable-backgrounding-occluded-windows',
        #     '--disable-breakpad',
        #     '--disable-client-side-phishing-detection',
        #     '--disable-component-update',
        #     '--disable-default-apps',
        #     '--disable-dev-shm-usage',
        #     '--disable-domain-reliability',
        #     '--disable-extensions',
        #     '--disable-features=AudioServiceOutOfProcess',
        #     '--disable-hang-monitor',
        #     '--disable-ipc-flooding-protection',
        #     '--disable-notifications',
        #     '--disable-offer-store-unmasked-wallet-cards',
        #     '--disable-popup-blocking',
        #     '--disable-print-preview',
        #     '--disable-prompt-on-repost',
        #     '--disable-renderer-backgrounding',
        #     '--disable-setuid-sandbox',
        #     '--disable-speech-api',
        #     '--disable-sync',
        #     '--disk-cache-size=33554432',
        #     '--hide-scrollbars',
        #     '--ignore-gpu-blacklist',
        #     '--ignore-certificate-errors',
        #     '--metrics-recording-only',
        #     '--mute-audio',
        #     '--no-default-browser-check',
        #     '--no-first-run',
        #     '--no-pings',
        #     '--no-sandbox',
        #     '--no-zygote',
        #     '--password-store=basic',
        #     '--use-gl=swiftshader',
        #     '--use-mock-keychain',
        #     '--single-process',
        #     '--headless']

        # #chrome_options.add_argument('--disable-gpu')
        # for argument in lambda_options:
        #     chrome_options.add_argument(argument)
        # chrome_options.add_argument('--user-data-dir={}'.format(self._tmp_folder + '/user-data'))
        # chrome_options.add_argument('--data-path={}'.format(self._tmp_folder + '/data-path'))
        # chrome_options.add_argument('--homedir={}'.format(self._tmp_folder))
        # chrome_options.add_argument('--disk-cache-dir={}'.format(self._tmp_folder + '/cache-dir'))

        return chrome_options
