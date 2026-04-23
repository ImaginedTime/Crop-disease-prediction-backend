"""
Batch script to label corn images by disease.
Loads the corn model, predicts disease for each image in images/corn/,
and copies them into labelled_images/corn/<disease>/ folders.
"""

import os
import sys
import shutil
import gc

import tensorflow as tf
import numpy as np
from PIL import Image
from tqdm import tqdm

# Base directory (project root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Paths
IMAGES_DIR = os.path.join(BASE_DIR, 'images', 'corn')
OUTPUT_DIR = os.path.join(BASE_DIR, 'labelled_images', 'corn')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'corn_2.h5')

# Class names (from main.py)
CORN_CLASS_NAMES = [
    'CORN COMMON RUST',
    'CORN GREY LEAF SPOT',
    'CORN HEALTHY',
    'CORN NORTHERN LEAF BLIGHT',
]

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif'}


def load_and_preprocess_image(image_path):
    """Load an image file, convert to RGB, resize to 224x224, and normalize."""
    image = Image.open(image_path).convert('RGB')
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


def predict_disease(model, image_array):
    """Run prediction and return the class name and confidence."""
    prediction = model.predict(image_array, verbose=0)
    predicted_class = CORN_CLASS_NAMES[np.argmax(prediction)]
    confidence = float(np.max(prediction))
    return predicted_class, confidence


def main():
    # Validate paths
    if not os.path.isdir(IMAGES_DIR):
        print(f"ERROR: Images directory not found: {IMAGES_DIR}")
        sys.exit(1)

    if not os.path.isfile(MODEL_PATH):
        print(f"ERROR: Model file not found: {MODEL_PATH}")
        sys.exit(1)

    # Collect all image files
    image_files = [
        f for f in os.listdir(IMAGES_DIR)
        if os.path.isfile(os.path.join(IMAGES_DIR, f))
        and os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]

    if not image_files:
        print(f"No images found in {IMAGES_DIR}")
        sys.exit(0)

    print(f"Found {len(image_files)} images in {IMAGES_DIR}")
    print(f"Loading model from {MODEL_PATH}...")

    # Load model once
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully.\n")

    # Counters
    counts = {name: 0 for name in CORN_CLASS_NAMES}
    errors = 0

    for filename in tqdm(image_files, desc="Labelling", unit="img"):
        src_path = os.path.join(IMAGES_DIR, filename)

        try:
            image_array = load_and_preprocess_image(src_path)
            predicted_class, confidence = predict_disease(model, image_array)

            # Create output folder using the disease name
            disease_folder = os.path.join(OUTPUT_DIR, predicted_class)
            os.makedirs(disease_folder, exist_ok=True)

            # Copy image to the labelled folder
            dst_path = os.path.join(disease_folder, filename)
            shutil.copy2(src_path, dst_path)

            counts[predicted_class] += 1
            tqdm.write(f"{filename} -> {predicted_class} ({confidence:.2%})")

        except Exception as e:
            errors += 1
            tqdm.write(f"ERROR processing {filename}: {e}")

    # Cleanup
    del model
    gc.collect()

    # Summary
    print("\n" + "=" * 50)
    print("LABELLING COMPLETE")
    print("=" * 50)
    for class_name, count in counts.items():
        print(f"  {class_name}: {count}")
    print(f"  Errors: {errors}")
    print(f"  Total: {len(image_files)}")
    print(f"\nLabelled images saved to: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
