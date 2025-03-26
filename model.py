import os
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # hide INFO messages

class ImageClassifier:
    def __init__(self):
        self.model = load_model("image_classifier/Hot_or_Not.keras")
        print("Model loaded successfully.")

    def preprocess_image(self, img_path, img_size=(224, 224)):
        img = image.load_img(img_path, target_size=img_size)
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict(self, img_path):
        img_array = self.preprocess_image(img_path)
        prediction = self.model.predict(img_array)
        confidence = prediction[0][0]
        if confidence > 0.5:
            print(f"✅ LIKE ({confidence * 100:.2f}% confidence)")
        else:
            print(f"❌ DON'T LIKE ({1 - confidence * 100:.2f}% confidence)")



classifier = ImageClassifier()
img_path = "./image_classifier/test_set/like/HotChick.jpg"
classifier.predict(img_path)

