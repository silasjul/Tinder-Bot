import time
import random
from tqdm import tqdm
import selenium
from scripts.browser_controller import BrowserController
from scripts.model import HotOrNot
import time

tinder = BrowserController()
classifier = HotOrNot(visualize_predictions=True)

while True:
    can_swipe = True
    number_of_matches = len(tinder.get_match_urls())

    # Swiping
    print("Beginning to swipe 🫷")
    while can_swipe:
        # Predict swipe
        image_path = tinder.get_girl_img()
        label, confidence = classifier.predict_image(image_path)

        try:
            if (label == 'like'): 
                tinder.click_like()
                if len(tinder.get_match_urls()) > number_of_matches: # We got a match!
                    tinder.reset()
            elif (label == 'dislike'): 
                tinder.click_dislike()
        except(selenium.common.exceptions.ElementClickInterceptedException):
            print("Cant swipe anymore 😭")
            can_swipe = False
            tinder.reset()

        time.sleep(2)

    # Texting
    print("Texting new matches 📝")
    for url in tinder.get_match_urls():
        tinder.go_url(url)
        tinder.send_message("Du ser godt ud 😍") # Default starter message
    
    # for message in chats
        # get messages
        # if new message (i didnt send last message)
            # if she accepted date
                # notify me
            # Send msg

        # Else if lastmsg over 24h ago
            # Send msg

    sleep_timer = random.randint(45, 60)
    print(f"Going to sleep for {sleep_timer} minutes 😴")
    for minute in tqdm(range(sleep_timer), desc="Sleeping Zzz..."):
        time.sleep(60) # sleep one minute