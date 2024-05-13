import tensorflow as tf
from keras.src.legacy.preprocessing.image import ImageDataGenerator

# Define the model architecture with dropout
def create_eye_state_model(input_shape):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),  # Dropout layer with dropout rate of 0.5
        tf.keras.layers.Dense(1, activation='sigmoid')  # Output layer with sigmoid activation for binary classification
    ])

    return model

# Create the model
input_shape = (100, 100, 3)
model = create_eye_state_model(input_shape)

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Define paths to your dataset
data_dir = r'C:\Users\omer\Desktop\dataset-faces\dataset'

# Define image dimensions and batch size
img_width, img_height = 100, 100
batch_size = 32

# Create data generators with augmentation for both training and validation
datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

train_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    subset='training'  # Use 85% of the data for training
)

validation_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation'  # Use 15% of the data for validation
)

# Implement early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',  # Monitor validation loss
    patience=3,  # Stop training if no improvement after 3 epochs
    restore_best_weights=True  # Restore weights to the best model
)

# Train the model with early stopping
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size,
    callbacks=[early_stopping]  # Pass the early stopping callback
)

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(validation_generator)
print('Test accuracy:', test_accuracy)

# Save the trained model
model.save('face_eyes_state_detection_model.h5')
