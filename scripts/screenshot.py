import pyautogui
import time

async def getImage():
    time.sleep(1)
    screenshot = pyautogui.screenshot()
    return screenshot.crop((961, 220, 1335, 690)) # left, upper, right, lower