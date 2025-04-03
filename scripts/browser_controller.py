import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from glob import glob
from PIL import Image
from messages import MessageGenerator

class BrowserController():
    def __init__(self):
        chrome_profile_path = r"C:\Users\silas\AppData\Local\Google\Chrome\User Data"

        # Driver options
        self.options = Options()
        self.options.add_argument(f"--user-data-dir={chrome_profile_path}") # access to my chrome pass, cookies, history, etc.
        self.options.add_argument("--profile-directory=Default") # use my default profile
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Avoid bot detection
        self.options.add_experimental_option("useAutomationExtension", False)

        # Initialize chrome driver and open Tinder
        self.driver = webdriver.Chrome(options=self.options)
        
        self.reset()

    def click_like(self):
        like_btn = self.driver.find_element(By.XPATH, '//button[.//span[text()="Like"]]')
        like_btn.click()

    def click_dislike(self):
        dislike_btn = self.driver.find_element(By.XPATH, '//button[.//span[text()="Nope"]]')
        dislike_btn.click()

    def get_match_urls(self):
        matches = self.driver.find_elements(By.XPATH, '//*[@id="q-675566543"]/ul/li/a')[1:] # First element is ad
        urls = [match.get_attribute("href") for match in matches]
        return urls
    
    def get_girl_img(self):
        img = self.driver.find_element(By.XPATH, '//*[@id="carousel-item-0"]/div')

        # Path
        image_amount = len(glob("./data/temp/*.png"))
        screenshot_path = f"./data/temp/{image_amount+1}.png"

        # Take screenshot
        img.screenshot(screenshot_path)

        # Crop the image to remove the Tinder UI
        with Image.open(screenshot_path) as im:
            crop_box = (0, 30, im.width, im.height - 130) # removes 50 pixels from top and 130 from bottom
            cropped_image = im.crop(crop_box)
            cropped_image.save(screenshot_path) # Overwrite image
    
        return screenshot_path
    
    def go_url(self, url):
        self.driver.get(url)
        time.sleep(5)
    
    def reset(self):
        self.driver.get("https://tinder.com/app/recs")
        time.sleep(5)

    def get_msg_log(self):
        messages = self.driver.find_elements(By.XPATH, '//*[@id="SC.chat_61b3a4fe521b470100053a0367e1ebd47fa7552ab991d0d3"]/div[4]/span')
        return [message.text for message in messages]

    def send_message(self, message):
        # Enter message
        text_area = self.driver.find_element(By.XPATH, '//*[@id="q-1313898230"]')
        self.driver.execute_script("arguments[0].value = arguments[1];", text_area, message) # Can't insert emojis with send_keys()
        text_area.send_keys(" ") # register with a space

        # Send message
        form = self.driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/div/div/div/div/div[1]/div/div/div[3]/form')
        form.submit()
    
if __name__ == "__main__":
    tinder = BrowserController()
    messenger = MessageGenerator()

    # go to match
    tinder.go_url(tinder.get_match_urls()[-1])

    # send message
    tinder.send_message("Du ser godt ud 😍")

    input("close browser...")
    

