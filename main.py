import time
import random
from tqdm import tqdm
from scripts.browser_controller import BrowserController, Message
from scripts.model import HotOrNot
from scripts.messages import MessageGenerator
import time

tinder = BrowserController()
classifier = HotOrNot(visualize_predictions=True)
messages = MessageGenerator()

opener = """
    Hvis jeg var en T-rex, ville jeg prøve at kramme dig med mine små arme 
    også ligge mig ned og græde fordi jeg ikke kunne 
    modstå din lækre menneskeduft og spise dig"""

while True:
    can_swipe = True
    new_matches = False

    # Phase 1: Swiping
    print("Phase 1: Let the swiping begin 🫷")
    while can_swipe:
        image_path = tinder.get_girl_img()
        prediction, confidence = classifier.predict_image(image_path)

        if (prediction == 'like'): 
            tinder.click_like()
        elif (prediction == 'dislike'): 
            tinder.click_dislike()
        
        if tinder.is_out_of_swipes():
            tinder.reset()
            can_swipe = False
        elif tinder.match_found(): # Fix
            tinder.reset()
            new_matches = True

    # Phase 2: Texting opener to new matches
    print("Phase 2: Texting new matches 📝")
    if new_matches:
        for url in tinder.get_match_urls():
            tinder.send_message()
        tinder.reset()

    # Phase 3: Texting existing matches
    print("Phase 3: Texting existing matches 💌")
    for url in tinder.get_message_urls():
        tinder.go_url(url)
        message_log = tinder.get_messages()

        last_msg: Message = tinder.get_messages()[-1]
        if last_msg.sender == "Me":
            time_from_msg_hours = round((time.time() - last_msg.datetime.timestamp()) / 3600, 1)
            if time_from_msg_hours > 24:
                print(f"Status: sending message after 24 hours, last message: {time_from_msg_hours} ago", )
                new_msg = messages.generate(message_log)
                tinder.send_message(new_msg)
            else:
                print(f"Status: last message sent {time_from_msg_hours} hours ago, skipping...")
                continue
        else:
            date_accepted = messages.analyse_message(str(last_msg))
            if date_accepted:
                print("HURRAY! She accepted the date! Go text her the details: ", url)
            else:
                print("Status: she didn't accept the date, sending new message")
                new_msg = messages.generate(message_log)
                tinder.send_message(new_msg)


    # Phase 4: Sleep
    sleep_timer = random.randint(5, 10) # minutes
    print(f"Going to sleep for {sleep_timer} minutes 😴")
    for minute in tqdm(range(sleep_timer), desc="Sleeping Zzz..."):
        time.sleep(60)

