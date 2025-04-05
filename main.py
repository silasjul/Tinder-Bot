import time
import random
from tqdm import tqdm
from scripts.browser_controller import BrowserController, Message
from scripts.model import HotOrNot
from scripts.messages import MessageGenerator
import selenium
import time

tinder = BrowserController()
classifier = HotOrNot(visualize_predictions=False)
messages = MessageGenerator()

opener = """Hvis jeg var en T-rex, ville jeg prøve at kramme dig med mine små arme 
    også ligge mig ned og græde fordi jeg ikke kunne 
    modstå din lækre menneskeduft og spise dig"""

def sleep_random(min=0.5, max=1):
    time.sleep((random.random() * min) + max-min)

while True:
    time_to_swipe = 1 # swipe time
    time_start = time.time()

    # Phase 1: Swiping
    print("Phase 1: Let the swiping begin 🫷")
    while (time.time() - time_start) / 60 < time_to_swipe:
        print(f"Status: {time_to_swipe - (time.time() - time_start) / 60:.2f} minutes left")
        
        image_path = tinder.get_girl_img()
        prediction, confidence = classifier.predict_image(image_path)

        try:
            if (prediction == 'like'): 
                tinder.click_like()
            elif (prediction == 'dislike'): 
                tinder.click_dislike()
        except selenium.common.exceptions.ElementClickInterceptedException:
            tinder.reset() # Pop up is blocking the like/dislike button
        sleep_random()

    # Phase 2: Texting opener to new matches
    print("Phase 2: Texting new matches 📝")
    new_matches = tinder.get_match_urls()
    if (len(new_matches) > 0):
        for url in new_matches():
            tinder.go_url(url)
            tinder.send_message(opener)
            sleep_random(1, 2)
        tinder.reset()
    else:
        print("Status: no new matches found")

    # Phase 3: Texting existing matches
    print("Phase 3: Texting existing matches 💌")
    for url in tinder.get_message_urls():
        tinder.go_url(url)
        message_log = tinder.get_messages()

        last_msg: Message = tinder.get_messages()[-1]
        if last_msg.sender == "Her":
            print("Status: new message detected")
            date_accepted = messages.analyse_message(str(last_msg))
            if date_accepted:
                print("HURRAY! She accepted the date! Go text her the details: ", url)
            else:
                print("Status: sending response...")
                new_msg = messages.generate(message_log)
                tinder.send_message(new_msg)
                sleep_random(1, 2)
        else:
            print(f"Status: no new messages from {last_msg.name}, last message was: {(time.time()-last_msg.datetime.timestamp())/3600:.2f} hours ago")
    
    tinder.reset()

