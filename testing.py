from PIL import Image
import os
import pytesseract

words = []
directory = "pics"

for entry in os.scandir(directory):
    image = Image.open(entry.path)
    image = image.convert('L')
    text = pytesseract.image_to_string(image)
    words += [word for word in text.split()]
    #display(image)
print(words)

# TODO break down words into parts using NLTK and mad lib
