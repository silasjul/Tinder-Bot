import time
import pytest
from src.messages import MessageGenerator

@pytest.fixture
def messages():
    time.sleep(1) # Don't spam API
    return MessageGenerator()

def test_generate_opener(messages):
    bio = "I love hiking and dogs!"
    opener = messages.generate_opener(bio)
    assert isinstance(opener, str), "Opener should be a string"
    assert len(opener) > 0, "Opener should not be empty"

def test_analyse_msg_log(messages):
    message = ["Me: Hey do you want to go on a date?", "Her: That a great idea! I just don't have the time this week :'("]
    date_accepted = messages.analyse_msg_log(message)
    assert isinstance(date_accepted, bool), "Response shoulde be a boolean"