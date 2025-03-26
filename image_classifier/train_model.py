import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore

IMG_SIZE = (224, 224)      # Width and height of input images
BATCH_SIZE = 32            # Number of images processed in each training step
DATASET_PATH = "./image_classifier/dataset"
TEST_SET_PATH = "./image_classifier/test_set"

# Create an ImageDataGenerator for data augmentation and normalization
datagen = ImageDataGenerator(
    rescale=1./255,          
    rotation_range=30,       
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
)

# Load training data
train_data = datagen.flow_from_directory(
    DATASET_PATH,           
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",    # Binary classification (like vs dont like)
)

# Load EfficientNetB0 without the top layer
base_model = tf.keras.applications.EfficientNetB0(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze pretrained layers (prevent them from being updated during training)
base_model.trainable = False

# Create the model
model = tf.keras.Sequential([
    base_model,                                       # Pre-trained base model
    tf.keras.layers.GlobalAveragePooling2D(),         # Convert 2D feature maps to vectors
    tf.keras.layers.Dense(128, activation="relu"),    # Hidden layer with 128 neurons, ReLU activation
    tf.keras.layers.Dropout(0.3),                     # Randomly drop 30% of connections to prevent relying on top layer too much
    tf.keras.layers.Dense(1, activation="sigmoid")    # Output layer: 1 neuron with sigmoid for binary classification
])

# Compile the model
model.compile(
    optimizer="adam",              # Adam optimization algorithm
    loss="binary_crossentropy",    # Loss function for binary classification
    metrics=["accuracy"]           # Track accuracy during training
)

# Train the model
history = model.fit(
    train_data,                    
    epochs=10,                     # Number of complete passes through the dataset
)

# Validating model
test_datagen = ImageDataGenerator(
    rescale=1./255               # Only normalize pixels, no augmentation for testing
)

# Load the test data
test_data = test_datagen.flow_from_directory(
    TEST_SET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
)

# Evaluation
test_loss, test_acc = model.evaluate(test_data)
print(f"Test accuracy: {test_acc * 100:.2f}%")

model.save("Hot_or_Not.keras")