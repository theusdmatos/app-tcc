import os
import tensorflow as tf
import numpy as np
from flask import Flask, render_template, request, send_from_directory
app = Flask(__name__)  # Variavel que controlar nossa aplicação

dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

# Carregando o modelo que treinei e salvei no Kaggle
cnn_model = tf.keras.models.load_model('static/models/tcc.h5')
IMAGE_SIZE = 250

# Pré processamento das imagens que vamos testar


def preprocess_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [IMAGE_SIZE, IMAGE_SIZE])

# Os dados que entram nas redes neurais geralmente devem ser normalizados de alguma forma para torná-los mais acessíveis ao processamento pela rede.

# Normalizando
    image /= 255.0
    return image

# Lendo a imagem e pré processando


def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)

# Predição e classificação


def classify(cnn_model, image_path):

    preprocessed_image = load_and_preprocess_image(image_path)
    preprocessed_image = tf.reshape(
        preprocessed_image, (1, IMAGE_SIZE, IMAGE_SIZE, 3)
    )

    pred = cnn_model.predict(preprocessed_image)
    predNum = np.argmax(pred)

    if predNum == 0:
        label = ("{:2.0f}%".format(100*np.max(pred)) + " - Normal")

    elif predNum == 1:
        label = ("{:2.0f}%".format(100*np.max(pred)) + " - Tuberculose")

    return label, pred

# Rota para "/"


@app.route("/")
def home():
    return render_template("index.html")

# Rota para "/classify"


@app.route("/classify", methods=["POST", "GET"])
def upload_file():

    if request.method == "GET":
        return render_template("index.html")

    else:
        file = request.files["image"]
        upload_image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        print(upload_image_path)
        file.save(upload_image_path)

        label, pred = classify(cnn_model, upload_image_path)
    return render_template(
        "classify.html", image_file_name=file.filename, label=label, pred=pred
    )


@app.route("/classify/<filename>")
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


port = int(os.getenv('PORT', 8000))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
