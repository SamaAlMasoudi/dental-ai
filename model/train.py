import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# تجهيز الصور
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train = datagen.flow_from_directory(
    '../dataset',
    target_size=(224,224),
    batch_size=16,
    class_mode='categorical',
    subset='training'
)

val = datagen.flow_from_directory(
    '../dataset',
    target_size=(224,224),
    batch_size=16,
    class_mode='categorical',
    subset='validation'
)

# بناء الموديل
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32,(3,3),activation='relu',input_shape=(224,224,3)),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# تجهيز التدريب
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# تدريب
model.fit(train, validation_data=val, epochs=5)

# حفظ الموديل
model.save("../model.h5")
