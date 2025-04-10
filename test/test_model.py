import pytest
from src.model import HotOrNot

@pytest.fixture
def classifier():
    return HotOrNot(visualize_predictions=False)

def test_predict_image(classifier):
    image_path = "test/test.jpg"
    prediction, confidence = classifier.predict_image(image_path)
    assert prediction in ['like', 'dislike'], "Prediction should be 'like' or 'dislike'"
    assert 0 <= confidence <= 100, "Confidence should be between 0 and 100"