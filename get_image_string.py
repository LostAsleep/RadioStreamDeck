import base64

IMG_FILE = "./Assets/Pressed.png"


with open(IMG_FILE, "rb") as image_file:
    image_data_base64_encoded_string = base64.b64encode(image_file.read())

print(image_data_base64_encoded_string)