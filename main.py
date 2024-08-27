import tensorflow as tf

from fastapi import FastAPI, UploadFile, File, Request

from PIL import Image
import numpy as np
import io

app = FastAPI()

# Soybean ['SOYABEAN BACTERIAL LEAF BLIGHT', 'SOYABEAN DRY LEAF', 'SOYABEAN HEALTHY', 'SOYABEAN SEPTORIA BROWN SPOT', 'SOYABEAN VEIN NECROSIS'] [0.96]


ground_nut_class_names = ['GROUNDNUT  LEAF SPOT (EARLY AND LATE)', 'GROUNDNUT  ROSETTE', 'GROUNDNUT  RUST', 'GROUNDNUT ALTERNARIA LEAF SPOT', 'GROUNDNUT HEALTHY']
wheat_class_names = ['WHEAT BROWN RUST', 'WHEAT HEALTHY', 'WHEAT YELLOW RUST']
rice_class_names = ['RICE BACTERIAL BLIGHT', 'RICE BLAST', 'RICE HEALTHY', 'RICE NECK BLAST']
corn_class_names = ['CORN COMMON RUST', 'CORN GREY LEAF SPOT', 'CORN HEALTHY', 'CORN NORTHERN LEAF BLIGHT']
potato_class_names = ['POTATO EARLY BLIGHT', 'POTATO HEALTHY', 'POTATO LATE BLIGHT']
sugarcane_class_names = ['SUGARCANE BACTERIAL BLIGHT', 'SUGARCANE HEALTHY', 'SUGARCANE RED ROT', 'SUGARCANE YELLOW RUST']
tea_class_names = ['TEA ALGAL LEAF', 'TEA ANTRACNOSE', 'TEA HEALTHY', 'TEA LEAF BLIGHT', 'TEA RED LEAF SPOT', 'TEA RED SCAB']
soyabean_class_names = ['SOYABEAN BACTERIAL LEAF BLIGHT', 'SOYABEAN DRY LEAF', 'SOYABEAN HEALTHY', 'SOYABEAN SEPTORIA BROWN SPOT', 'SOYABEAN VEIN NECROSIS']


crops = ['groundnut', 'wheat', 'rice', 'corn', 'potato', 'sugarcane', 'tea', 'soyabean']

# function that returns the model and class names based on the crop type
def get_model_and_class_names(crop_type):
    if crop_type == 'groundnut':
        ground_nut_model = tf.keras.models.load_model('./models/ground_nut_2.h5')
        return ground_nut_model, ground_nut_class_names
    elif crop_type == 'wheat':
        wheat_model = tf.keras.models.load_model('./models/wheat_2.h5')
        return wheat_model, wheat_class_names
    elif crop_type == 'rice':
        rice_model = tf.keras.models.load_model('./models/rice_2.h5')
        return rice_model, rice_class_names
    elif crop_type == 'corn':
        corn_model = tf.keras.models.load_model('./models/corn_2.h5')
        return corn_model, corn_class_names
    elif crop_type == 'potato':
        potato_model = tf.keras.models.load_model('./models/potato_2.h5')
        return potato_model, potato_class_names
    elif crop_type == 'sugarcane':
        sugarcane_model = tf.keras.models.load_model('./models/sugarcane_2.h5')
        return sugarcane_model, sugarcane_class_names
    elif crop_type == 'tea':
        tea_model = tf.keras.models.load_model('./models/tea_2.h5')
        return tea_model, tea_class_names
    elif crop_type == 'soyabean':
        soyabean_model = tf.keras.models.load_model('./models/soyabean_2.h5')
        return soyabean_model, soyabean_class_names

# function that converts the image to the required format
def convert_jpg_to_jpeg(image: UploadFile):
    image = Image.open(io.BytesIO(image.file.read()))
    image = image.convert('RGB')
    return image

@app.get('/')
async def root():
    return {"message": "Welcome to the Crop Disease Detection API"}


@app.post('/predict')
async def predict(crop_type = "groundnut", image: UploadFile = File(...)):
    if crop_type not in crops:
        return {"error": "Invalid crop type"}

    try:
        image = convert_jpg_to_jpeg(image)
        image = image.resize((224, 224))
        image = np.array(image)
        image = image / 255.0
        image = np.expand_dims(image, 0)

        model, class_names = get_model_and_class_names(crop_type)

        prediction = model.predict(image)
        predicted_class = class_names[np.argmax(prediction)]

        return {"class": predicted_class, "confidence": float(np.max(prediction))}

    except Exception as e:
        return {"error": str(e)}