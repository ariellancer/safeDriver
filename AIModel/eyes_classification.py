import tensorflow as tf


from keras.src.legacy.preprocessing.image import ImageDataGenerator


# Define the model architecture
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
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')  # Output layer with sigmoid activation for binary classification
    ])

    return model


# Create the model
input_shape = (100, 100, 3)  # Define the input shape based on your image size
model = create_eye_state_model(input_shape)

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Display the model summary
model.summary()
# Define paths to your dataset
train_data_dir = r'C:\Users\omer\Desktop\dataset-eyes\dataset\train'
validation_data_dir = r'C:\Users\omer\Desktop\dataset-eyes\dataset\test'

# Define image dimensions and batch size
img_width, img_height = 100, 100
batch_size = 32

# Create data generators with augmentation
train_datagen = ImageDataGenerator(
    rescale=1. / 255,  # Rescale pixel values to [0, 1]
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary'  # Since we have two classes (open and closed eyes)
)

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary'
)

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=10,  # You can adjust the number of epochs as needed
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)
test_loss, test_accuracy = model.evaluate(validation_generator)
print('Test accuracy:', test_accuracy)
# Save the trained model
model.save('eye_state_detection_model.h5')
