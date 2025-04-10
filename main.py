print(r"""
,---------. .-./`) ,---.   .--. ______         .-''-.  .-------.             _______       ,-----.  ,---------.  
\          \\ .-.')|    \  |  ||    _ `''.   .'_ _   \ |  _ _   \           \  ____  \   .'  .-,  '.\          \ 
 `--.  ,---'/ `-' \|  ,  \ |  || _ | ) _  \ / ( ` )   '| ( ' )  |           | |    \ |  / ,-.|  \ _ \`--.  ,---' 
    |   \    `-'`"`|  |\_ \|  ||( ''_'  ) |. (_ o _)  ||(_ o _) /           | |____/ / ;  \  '_ /  | :  |   \    
    :_ _:    .---. |  _( )_\  || . (_) `. ||  (_,_)___|| (_,_).' __         |   _ _ '. |  _`,/ \ _/  |  :_ _:    
    (_I_)    |   | | (_ o _)  ||(_    ._) ''  \   .---.|  |\ \  |  |        |  ( ' )  \: (  '\_/ \   ;  (_I_)    
   (_(=)_)   |   | |  (_,_)\  ||  (_.\.' /  \  `-'    /|  | \ `'   /        | (_{;}_) | \ `"/  \  ) /  (_(=)_)   
    (_I_)    |   | |  |    |  ||       .'    \       / |  |  \    /         |  (_,_)  /  '. \_/``".'    (_I_)    
    '---'    '---' '--'    '--''-----'`       `'-..-'  ''-'   `'-'          /_______.'     '-----'      '---'    
                                                                                                                 
""")
print("Hi, im Siri. I got crazy RIZZ!!!\nLoading...")

import time
import random
from src.browser_controller import BrowserController
from src.model import HotOrNot
from src.messages import MessageGenerator
import time
import json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

tinder = BrowserController()
classifier = HotOrNot(visualize_predictions=config["visualize_predictions"])
messages = MessageGenerator()

def sleep_random(min=0.5, max=1):
    time.sleep((random.random() * min) + max-min)

def get_time_swiped(start_time):
    return (time.time() - start_time) / 60

while True:
    time_to_swipe = config["time_to_swipe"]
    out_of_swipes = False
    time_start = time.time()

    # Phase 1: Swiping
    print("Phase 1: Let the swiping begin 🫷")
    while get_time_swiped(time_start) < time_to_swipe and not out_of_swipes:
        print(f"Status: {time_to_swipe - get_time_swiped(time_start):.2f} minutes left")
        
        image_path = tinder.get_girl_img()
        prediction, confidence = classifier.predict_image(image_path)

        if (prediction == 'like'): 
            tinder.click_like()
        elif (prediction == 'dislike'): 
            tinder.click_dislike()

        time.sleep(0.5) # Wait for superlike popup to load
        tinder.close_superlike_popup()
        sleep_random()

    # Phase 2: Texting opener to new matches
    print("Phase 2: Texting new matches 📝")
    new_matches = tinder.get_match_urls()
    if (len(new_matches) > 0):
        for url in new_matches:
            tinder.go_url(url)
            bio = tinder.get_bio()
            opener = messages.generate_opener(bio)
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
        message_log_str = [str(msg) for msg in message_log]
        last_msg = message_log[-1]

        if last_msg.sender == "Her":
            print("Status: new message detected")
            date_accepted = messages.analyse_msg_log(message_log_str)
            if date_accepted:
                print("HURRAY! She accepted the date! Texting her the details...")
                new_msg = messages.generate_date(message_log_str)
                tinder.send_message(new_msg)
            else:
                print("Status: sending response...")
                new_msg = messages.generate_response(message_log_str)
                tinder.send_message(new_msg)
            sleep_random(1, 2)
        else:
            print(f"Status: no new messages from {last_msg.name}, last message was: {(time.time()-last_msg.datetime.timestamp())/3600:.2f} hours ago")
    
    tinder.reset()

