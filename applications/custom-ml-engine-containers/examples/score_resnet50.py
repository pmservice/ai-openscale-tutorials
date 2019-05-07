from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import requests
import json

IMAGE_PATH = '../images/fafel.png'
SERVER_HTTP = 'http://0.0.0.0:5000'
SCORING_RESNET50_ENDPOINT = SERVER_HTTP + '/v1/deployments/resnet50/online'


def prepare_payload(images_paths):
    images_list = []

    for image_path in images_paths:
        image = Image.open(image_path)

        if image.mode is not "RGB":
            image = image.convert("RGB")

        image = image.resize((224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = imagenet_utils.preprocess_input(image)
        images_list.append(image.tolist())

    return {'values': images_list}


def main():
    print("\n\n******************************************")
    print("Load the image and prepare scoring payload (2 images) ...")
    payload = prepare_payload([IMAGE_PATH, IMAGE_PATH])

    print("Score the model ...")
    r = requests.post(SCORING_RESNET50_ENDPOINT, json=payload)

    print("Return predictions ...\n")
    print(str(r.json()))
    print("\n******************************************\n")


if __name__ == "__main__":
    main()
