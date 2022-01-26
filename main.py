import os 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from time import sleep

PROMISED_DOWN = 300
PROMISED_UP = 10
CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']
TWITTER_EMAIL = os.environ['TWITTER_EMAIL']
TWITTER_PASSWORD = os.environ['TWITTER_PASSWORD']

class InternetSpeedTwitterBot: 
    
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.upload = PROMISED_UP
        self.download = PROMISED_DOWN

    def get_internet_speed(self): 
        self.driver.get('https://www.speedtest.net/')
        self.driver.find_element_by_xpath('//span[@class="start-text"]').click()
        sleep(60)
        self.upload = self.driver.find_element_by_xpath('//span[@data-upload-status-value]').text
        self.download = self.driver.find_element_by_xpath('//span[@data-download-status-value]').text
        self.driver.quit()

    def tweet_at_provider(self, download_speed, upload_speed): 
        if download_speed < self.download and upload_speed < self.upload: 
            self.driver.get('https://twitter.com/')
            self.driver.find_element_by_xpath('//a[@href="/login"]').click()
            
            sleep(3)
            username = self.driver.find_element_by_xpath('//input[@autocomplete="username"]')
            username.send_keys(TWITTER_EMAIL)
            username.send_keys(Keys.ENTER)
            
            sleep(1)
            password = self.driver.find_element_by_xpath('//span[text()="Password"]')
            password.send_keys(TWITTER_PASSWORD)
            password.send_keys(Keys.ENTER)
            
            sleep(2)
            new_tweet = self.driver.find_element_by_xpath('//div[contains(@class, "public-DraftStyleDefault-block")]')
            new_tweet.send_keys(
                f'Hey Internet Provider, why is my internet speed {self.download}down/{self.upload}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?'
            )
            
            sleep(1)
            self.driver.find_element_by_xpath('//div[@role="button"]//span[text()="Tweet"]').click()
            
            sleep(1)
            self.driver.quit()

            
bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
 
bot.get_internet_speed()
bot.tweet_at_provider()