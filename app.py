
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image, UnidentifiedImageError
import time

app = Flask(__name__)
CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# Load trained CNN model
model = tf.keras.models.load_model("task6_cnn_model.keras")

# CIFAR-10 class names
class_names = [
    "Airplane",
    "Automobile",
    "Bird",
    "Cat",
    "Deer",
    "Dog",
    "Frog",
    "Horse",
    "Ship",
    "Truck"
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask API is running successfully!",
        "project": "Task 15 - Image Classification",
        "status": "healthy"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    start_time = time.perf_counter()

    if "image" not in request.files:
        return jsonify({
            "error": "No image uploaded. Use the 'image' field."
        }), 400

    file = request.files["image"]

    if not file.filename:
        return jsonify({
            "error": "Please select an image file."
        }), 400

    try:
        image = Image.open(file).convert("RGB")
        image = image.resize((32, 32))

        image_array = np.asarray(
            image, dtype=np.float32
        ) / 255.0

        image_array = np.expand_dims(
            image_array, axis=0
        )

        prediction = model.predict(
            image_array, verbose=0
        )

        predicted_index = int(
            np.argmax(prediction[0])
        )

        predicted_class = class_names[predicted_index]

        confidence = float(
            prediction[0][predicted_index] * 100
        )

        response_time_ms = (
            time.perf_counter() - start_time
        ) * 1000

        app.logger.info(
            "Prediction completed: class=%s, time_ms=%.2f",
            predicted_class, response_time_ms
        )

        return jsonify({
            "prediction": predicted_class,
            "confidence": round(confidence, 2),
            "response_time_ms": round(response_time_ms, 2)
        }), 200

    except UnidentifiedImageError:
        return jsonify({
            "error": "Invalid image. Upload a valid JPG or PNG file."
        }), 400

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed. Check the server logs."
        }), 500


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "Image is too large. Maximum size is 10 MB."
    }), 413


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
