import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from glob import glob
from PIL import Image

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
        self.wait = WebDriverWait(self.driver, 10)
        
        self.reset()

    def click_like(self):
        like_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[4]/div/div[4]/button')))
        like_btn.click()

    def click_dislike(self):
        dislike_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[4]/div/div[2]/button')))
        dislike_btn.click()

    def get_match_urls(self):
        matches = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[1]/div/aside/div/div/div/div/div/div[3]/div[1]/ul/li/a')[1:] # First element is ad
        urls = [match.get_attribute("href") for match in matches]
        return urls
    
    def get_message_urls(self):
        self.reset()

        messages_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/aside/div/div/div/div/div/div[2]/div/div[2]/button')))
        messages_btn.click()

        message_div = self.driver.find_element(By.CLASS_NAME, 'messageList')
        message_list = message_div.find_elements(By.XPATH, './ul/li/a')
        
        return [message.get_attribute("href") for message in message_list]
    
    def get_girl_img(self):
        img = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[2]/div[1]/section/div[2]/div[1]/div')))

        # Total amount of images
        dataset_amount = len(glob("./data/*/*/*.png"))
        temp_amount = len(glob("./data/*/*.png"))
        total = dataset_amount + temp_amount

        # Path
        screenshot_path = f"./data/temp/{total+1}.png"

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
    
    def reset(self):
        self.driver.get("https://tinder.com/app/recs")
        self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[2]/div[1]/section/div[2]/div[1]/div'))) # swiping image has loaded

    def send_message(self, message):
        # Enter message
        text_area = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/div[1]/div/div/div[3]/form/textarea')
        self.driver.execute_script("arguments[0].value = arguments[1];", text_area, message) # Can't insert emojis with send_keys()
        text_area.send_keys(" ") # js doesn't trigger the oninput event, so we need to send a space to trigger it

        # Send message
        form = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/div[1]/div/div/div[3]/form')
        form.submit()

    def is_out_of_swipes(self):
        temp = self.wait._timeout
        self.wait._timeout = 1
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div')))
            self.wait._timeout = temp
            return True
        except selenium.common.exceptions.TimeoutException:
            self.wait._timeout = temp
            return False
    
    def match_found(self):
        pass
    
if __name__ == "__main__":
    tinder = BrowserController()
    tinder.click_like()
    print(tinder.is_out_of_swipes())
    input("Press enter to exit...")

