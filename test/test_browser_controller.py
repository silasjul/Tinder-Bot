import pytest
from src.browser_controller import BrowserController

@pytest.fixture
def browser():
    browser = BrowserController()
    yield browser
    browser.quit()


def test_get_girl_img(browser):
    image_path = browser.get_girl_img()
    assert isinstance(image_path, str), "Image path should be a string"
    assert image_path.endswith(('.jpg', '.png')), "Image path should point to a valid image file"


def test_click_like(browser):
    result = browser.click_like()
    assert isinstance(result, bool), "Result should be a boolean"
    assert result is True, "Clicking like should return True"


def test_get_messages(browser):
    urls = browser.get_message_urls()
    assert isinstance(urls, list), "Should return a list"
    assert all(isinstance(url, str) for url in urls), "Each URL should be a string"


def test_get_bio(browser):
    bio = browser.get_bio()
    assert bio is None or isinstance(bio, str), "Bio should be None or a string"


def test_get_match_urls(browser):
    match_urls = browser.get_match_urls()
    assert isinstance(match_urls, list), "Match URLs should be a list"
    assert all(isinstance(url, str) for url in match_urls), "Each match URL should be a string"
