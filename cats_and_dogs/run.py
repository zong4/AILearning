import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, BatchNormalization, Activation, LeakyReLU
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import LearningRateScheduler

import os
import numpy as np
import matplotlib.pyplot as plt

# Get project files
# !wget https://cdn.freecodecamp.org/project-data/cats-and-dogs/cats_and_dogs.zip
# !unzip cats_and_dogs.zip
PATH = './cats_and_dogs/cats_and_dogs'
train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

# Get number of files in each directory. The train and validation directories
# each have the subdirecories "dogs" and "cats".
total_train = sum([len(files) for r, d, files in os.walk(train_dir)])
total_val = sum([len(files) for r, d, files in os.walk(validation_dir)])
total_test = len(os.listdir(test_dir))

# Variables for pre-processing and training.
batch_size = 128
epochs = 30
IMG_HEIGHT = 150
IMG_WIDTH = 150

train_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our training data
validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data
test_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our test data

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary')
val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                                directory=validation_dir,
                                                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                                class_mode='binary')
test_data_gen = test_image_generator.flow_from_directory(batch_size=total_test,
                                                            directory=test_dir,
                                                            target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                            class_mode='binary')

def plotImages(images_arr, probabilities = False):
    fig, axes = plt.subplots(len(images_arr), 1, figsize=(5,len(images_arr) * 3))
    if probabilities is False:
      for img, ax in zip( images_arr, axes):
          ax.imshow(img)
          ax.axis('off')
    else:
      for img, probability, ax in zip( images_arr, probabilities, axes):
          ax.imshow(img)
          ax.axis('off')
          if probability > 0.5:
              ax.set_title("%.2f" % (probability*100) + "% dog")
          else:
              ax.set_title("%.2f" % ((1-probability)*100) + "% cat")
    plt.show()

sample_training_images, _ = next(train_data_gen)
# plotImages(sample_training_images[:5])

train_image_generator = ImageDataGenerator(rescale=1./255,
                                          rotation_range=45,
                                          width_shift_range=.15,
                                          height_shift_range=.15,
                                          horizontal_flip=True,
                                          zoom_range=0.5) # Generator for our training data

# train_image_generator = ImageDataGenerator(
#     rescale=1./255,
#     rotation_range=45,  # 增大旋转范围
#     width_shift_range=0.3,  # 增大水平平移范围
#     height_shift_range=0.3,  # 增大垂直平移范围
#     shear_range=0.3,  # 增大错切范围
#     zoom_range=[0.7, 1.3],  # 更宽的缩放范围
#     horizontal_flip=True,
#     vertical_flip=True,  # 增加垂直翻转
#     fill_mode='nearest'
# )

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                     directory=train_dir,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     class_mode='binary')

augmented_images = [train_data_gen[0][0][0] for i in range(5)]
# plotImages(augmented_images)

model = Sequential([
    Conv2D(16, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    MaxPooling2D(),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(128, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    Dense(1)
])

# model = Sequential([
#     Conv2D(16, 3, padding='same', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
#     BatchNormalization(),
#     Activation('relu'),
#     MaxPooling2D(),
#     Conv2D(32, 3, padding='same'),
#     BatchNormalization(),
#     Activation('relu'),
#     MaxPooling2D(),
#     Conv2D(64, 3, padding='same'),
#     BatchNormalization(),
#     Activation('relu'),
#     MaxPooling2D(),
#     Conv2D(128, 3, padding='same'),
#     BatchNormalization(),
#     Activation('relu'),
#     MaxPooling2D(),
#     Flatten(),
#     Dense(512, activation='relu'),
#     tf.keras.layers.Dropout(0.5),
#     Dense(1)
# ])

model.summary()

model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

def cosine_annealing_lr(epoch, lr, T_max=100):
    return 0.001 * 0.5 * (1 + np.cos(np.pi * epoch / T_max))
lr_scheduler = LearningRateScheduler(cosine_annealing_lr)

history = model.fit(
    train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size,
    # callbacks=[lr_scheduler],
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()