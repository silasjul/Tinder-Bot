import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import random_split
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
import timm

import matplotlib.pyplot as plt
from tqdm import tqdm
from PIL import Image

model_path = "./hotornot_classifier.pt"

# Device configuration
if not torch.cuda.is_available():
    device = torch.device("cpu")
    print("GPU not available, using CPU instead.")
else:
    device = torch.device("cuda:0") # GPU is much faster than CPU!
    print(f"Using device: {device} ")


"""DATA"""

class TinderWomenDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data = ImageFolder(data_dir, transform=transform)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    @property
    def classes(self):
        return self.data.classes
    
transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

ds_folder = "./data/dataset"

ds = TinderWomenDataset(ds_folder, transform=transforms)

train_size = int(0.7 * len(ds))  # 80% for training
val_size = int(0.15 * len(ds))   # 15% for validation
test_size = len(ds) - train_size - val_size  # Remaining 5% for testing

train_ds, val_ds, test_ds = random_split(ds, [train_size, val_size, test_size])

train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)


"""DEFINE MODEL"""

class HotOrNotClassifier(nn.Module):
    def __init__(self, num_classes=2): # 2 classes - like or dislike
        super(HotOrNotClassifier, self).__init__()

        # Define model
        self.base_model = timm.create_model("efficientnet_b0", pretrained=True) # already trained on imageNet dataset
        self.features = nn.Sequential(*list(self.base_model.children())[:-1]) # remove pretrained classifier (last layer) to replace with our own classifier

        enet_out_size = 1280
        self.classifier = nn.Linear(enet_out_size, num_classes)

    def forward(self, x):
        # Connect parts and return result
        x = self.features(x)
        output = self.classifier(x)
        return output
    
    
"""TRAIN MODEL"""

model = HotOrNotClassifier().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

train_losses, val_losses = [], []

def train_model(epochs=10):
    for epoch in range(epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        for images, labels in tqdm(train_loader, desc="Training Loop"):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)
        train_loss = running_loss / len(train_loader.dataset)
        train_losses.append(train_loss)

        # Validation phase
        model.eval()
        running_loss = 0.0
        with torch.no_grad():
            for images, labels in tqdm(val_loader, desc="Validation Loop"):
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                running_loss += loss.item() * images.size(0)
        val_loss = running_loss / len(val_loader.dataset)
        val_losses.append(val_loss)

        print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")

    # Visualize training and validation loss
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.show()

    # Save the model
    torch.save(model.state_dict(), model_path)


"""TESTING/EVALUATION"""

model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

def display_result(image, probabilities, class_names):
    fig, axarr = plt.subplots(1, 2, figsize=(14, 7))
            
    # Display image
    axarr[0].imshow(image)
    axarr[0].axis("off")
    
    # Display predictions
    axarr[1].barh(class_names, probabilities)
    axarr[1].set_xlabel("Probability")
    axarr[1].set_title("Class Predictions")
    axarr[1].set_xlim(0, 1)

    plt.tight_layout()
    plt.show(block=False)
    plt.pause(3)
    plt.close()
    
    return model

def test_model(visualize_wrong_predictions=False, visualize_correct_predictions=False):
    class_names = ds.classes
    wrong_predictions_count = 0
    correct_predictions_count = 0
    confidence_list = []

    for image_tensor, label in tqdm(test_ds, desc="Testing"):
        with torch.no_grad():
            image_tensor = image_tensor.to(device).unsqueeze(0)
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            probabilities = probabilities.cpu().numpy().flatten()

            predicted_idx = probabilities.argmax() # Predicted class index [0 or 1] like/dislike
            confidence = probabilities[predicted_idx]*100

            confidence_list.append(confidence)

            if predicted_idx != label:
                wrong_predictions_count += 1

                if visualize_wrong_predictions:
                    image = image_tensor.squeeze().permute(1, 2, 0).cpu()
                    display_result(image, probabilities, class_names)
            else:
                correct_predictions_count += 1
                if visualize_correct_predictions:
                    image = image_tensor.squeeze().permute(1, 2, 0).cpu()
                    display_result(image, probabilities, class_names)

    acuracy = correct_predictions_count / (correct_predictions_count + wrong_predictions_count) * 100
    avr_confidence = sum(confidence_list) / len(confidence_list)

    print(f"Correct predictions: {correct_predictions_count}")
    print(f"Wrong predictions: {wrong_predictions_count}")
    print(f"Accuracy: {acuracy:.2f}%")
    print(f"Average confidence: {avr_confidence:.2f}%")


"""PREDICITON"""

class HotOrNot():
    def __init__(self, visualize_predictions=True):
        self.visualize_predictions = visualize_predictions
        self.class_names = ds.classes

    def preprocess_image(self, image_path, transform):
        image = Image.open(image_path).convert("RGB")
        return image, transform(image).unsqueeze(0)

    def predict_image(self, image_path):
        original_image, image_tensor = self.preprocess_image(image_path, transforms)
        with torch.no_grad():
            image_tensor = image_tensor.to(device)
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            probabilities = probabilities.cpu().numpy().flatten()

        predicted_idx = probabilities.argmax()
        predicted_class = self.class_names[predicted_idx]
        confidence = probabilities[predicted_idx] * 100

        if self.visualize_predictions:
                    display_result(original_image, probabilities, self.class_names)

        return (predicted_class, confidence)
    

if __name__ == "__main__":
    # Create model
    #train_model(epochs=10)
    test_model(visualize_wrong_predictions=True, visualize_correct_predictions=False)