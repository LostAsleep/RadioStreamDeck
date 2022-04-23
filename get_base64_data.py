import base64

FILE = "./Assets/Roboto-Regular.ttf"


with open(FILE, "rb") as fhand:
    data_base64_encoded_string = base64.b64encode(fhand.read())

# with open("output.txt", "wb") as fhand:
#     fhand.write(data_base64_encoded_string)

print(data_base64_encoded_string)