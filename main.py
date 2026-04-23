import tensorflow as tf

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

import requests
import csv

from PIL import Image
import numpy as np
import io

# garbage collector to free up memory by deleting the loaded model from memory
import gc


app = FastAPI()

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# list of crops
crops = ['groundnut', 'wheat', 'rice', 'corn', 'potato', 'sugarcane', 'tea', 'soyabean', 'cotton', 'tomato']
langs = ['en', 'hi', 'tm', 'tl', 'kn', 'ml', 'gj', 'bg', 'od', 'pn', 'ma']

# sheet with content (public - anyone with the link can view)
sheet_id = "1Gf4fp710E9RN6PA8c0II2kn90d-_qZ_Q21GDYqzwKts"


# class names for each crop
ground_nut_class_names = ['GROUNDNUT LEAF SPOT (EARLY AND LATE)', 'GROUNDNUT ROSETTE', 'GROUNDNUT RUST', 'GROUNDNUT ALTERNARIA LEAF SPOT', 'GROUNDNUT HEALTHY']
wheat_class_names = ['WHEAT BROWN RUST', 'WHEAT HEALTHY', 'WHEAT YELLOW RUST']
rice_class_names = ['RICE BACTERIAL BLIGHT', 'RICE BLAST', 'RICE HEALTHY', 'RICE NECK BLAST']

corn_class_names = ['CORN COMMON RUST', 'CORN GREY LEAF SPOT', 'CORN HEALTHY', 'CORN NORTHERN LEAF BLIGHT']
# corn_class_names = ['CORN COMMON RUST', 'CORN HEALTHY', 'CORN NORTHERN LEAF BLIGHT']

potato_class_names = ['POTATO EARLY BLIGHT', 'POTATO HEALTHY', 'POTATO LATE BLIGHT']
sugarcane_class_names = ['SUGARCANE BACTERIAL BLIGHT', 'SUGARCANE HEALTHY', 'SUGARCANE RED ROT', 'SUGARCANE YELLOW RUST']
tea_class_names = ['TEA ALGAL LEAF', 'TEA ANTRACNOSE', 'TEA HEALTHY', 'TEA LEAF BLIGHT', 'TEA RED LEAF SPOT', 'TEA RED SCAB']
soyabean_class_names = ['SOYABEAN BACTERIAL LEAF BLIGHT', 'SOYABEAN DRY LEAF', 'SOYABEAN HEALTHY', 'SOYABEAN SEPTORIA BROWN SPOT', 'SOYABEAN VEIN NECROSIS']
cotton_class_names = ['COTTON APHIDS', 'COTTON ARMY WORM', 'COTTON BACTERIAL BLIGHT', 'COTTON HEALTHY', 'COTTON POWDERY MILDEW', 'COTTON TARGET SPOT']
tomato_class_names = ['TOMATO BACTERIAL SPOT', 'TOMATO EARLY BLIGHT', 'TOMATO HEALTHY', 'TOMATO LATE BLIGHT', 'TOMATO LEAF MOLD', 'TOMATO MOSAIC VIRUS', 'TOMATO SEPTORIA LEAF SPOT', 'TOMATO TARGET SPOTS', 'TOMATO YELLOW LEAF CURL VIRUS']


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
    elif crop_type == 'cotton':
        cotton_model = tf.keras.models.load_model('./models/cotton_2.h5')
        return cotton_model, cotton_class_names
    elif crop_type == 'tomato':
        tomato_model = tf.keras.models.load_model('./models/tomato_2.h5')
        return tomato_model, tomato_class_names

def convert_jpg_to_jpeg(image: UploadFile):
    try:
        image_data = image.file.read()
        print(f"Image data size: {len(image_data)} bytes")
        
        # Open the image using PIL
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGB')
        return image

    except Exception as e:
        raise ValueError(f"Error converting image: {e}")

def fetch_sheet_as_dicts(sheet_id, sheet_name):
    """Fetch a public Google Sheet tab as a list of dicts via CSV export."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    response = requests.get(url)
    response.raise_for_status()

    # Parse CSV into list of dicts, filtering out empty-string keys from trailing commas
    reader = csv.DictReader(io.StringIO(response.text))
    return [{k: v for k, v in row.items() if k} for row in reader]

def get_sheet_content(sheet_id, class_name, lang_code, is_disease=True):
    sheet_name = f"{lang_code}-diseases" if is_disease else f"{lang_code}-healthy"

    print(f"Sheet name: {sheet_name} - is a disease: {is_disease}")

    data = fetch_sheet_as_dicts(sheet_id, sheet_name)

    for row in data:
        if is_disease and row.get("Disease Name", "").strip().lower() in class_name.lower():
            return row
        if row.get("Crop Name", "").strip().lower() in class_name.lower():
            return row
    return None

def get_crop_info(prediction, crop_name, lang_code, sheet_id):
    is_healthy = "HEALTHY" in prediction.upper()
    
    content = get_sheet_content(sheet_id, prediction, lang_code, is_disease = not is_healthy)
    
    if content:
        return content
    else:
        return {"error": "No content found for the given crop and language"}

@app.get('/')
async def root():
    return {"message": "Welcome to the Crop Disease Detection API"}


@app.post('/predict/')
async def predict(crop_type: str = Form(...), lang: str = Form(...), image: UploadFile = File(...)):
    # crop_type = payload.crop_type
    # lang = payload.lang
    # image = payload.image.file

    print(crop_type)
    print(lang)

    lang = lang.lower()

    if crop_type not in crops:
        return {"error": f"Invalid crop type{crop_type}"}

    if lang not in langs:
        return {"error": f"Invalid language{lang}"}

    try:
        image = convert_jpg_to_jpeg(image)
        image = image.resize((224, 224))
        image = np.array(image)
        image = image / 255.0
        image = np.expand_dims(image, 0)

        model, class_names = get_model_and_class_names(crop_type)

        prediction = model.predict(image)
        predicted_class = class_names[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        del model
        gc.collect()

        print(predicted_class, confidence)

        crop_info = get_crop_info(predicted_class, crop_type, lang, sheet_id)

        return {
            "class": predicted_class, 
            "confidence": confidence, 
            "info": crop_info
        }

    except Exception as e:
        return {"error": str(e)}