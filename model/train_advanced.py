import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import os

# 1. إعدادات البيانات
# يفضل الآن أن يكون لديك 5 مجلدات داخل dataset:
# (Healthy, Caries, Infection, Fractured, BDC-BDR)
DATASET_PATH = '../dataset' 
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30 # زيادة عدد الدورات للوصول لدقة أعلى

# 2. تجهيز البيانات مع Augmentation مكثف لرفع الدقة
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest',
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# 3. بناء النموذج باستخدام MobileNetV2 مع Fine-tuning
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = True

# تجميد أول 100 طبقة فقط وتدريب الباقي لرفع الدقة
for layer in base_model.layers[:100]:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.4)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)
predictions = Dense(len(train_generator.class_indices), activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# 4. تقنيات متقدمة للتحكم في التدريب
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.00001)

# 5. تجهيز التدريب
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 6. التدريب
print(f"Classes found: {train_generator.class_indices}")
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=EPOCHS,
    callbacks=[early_stop, reduce_lr]
)

# 7. حفظ النموذج والبيانات
model.save("../model.h5")
with open("../classes.txt", "w") as f:
    # حفظ الترتيب الصحيح للفئات لاستخدامه في app.py
    indices = {v: k for k, v in train_generator.class_indices.items()}
    for i in range(len(indices)):
        f.write(f"{indices[i]}\n")

print("Training complete. Model and classes saved.")
