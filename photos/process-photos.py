from PIL import Image
import datetime
import os

# Load the template

os.chdir(os.path.dirname(os.path.realpath(__file__)))

template = Image.open("template.jpg")

# Create the composite
template.paste(Image.open("image1.jpg").resize((559, 419)), (30, 408))
template.paste(Image.open("image2.jpg").resize((559, 419)), (610, 408))
template.paste(Image.open("image3.jpg").resize((559, 419)), (30, 853))
template.paste(Image.open("image4.jpg").resize((559, 419)), (610, 853))

template = template.transpose(Image.FLIP_TOP_BOTTOM)

# Save it!
filename = os.path.dirname(os.path.realpath(__file__)) + "/archive/" + datetime.datetime.today().strftime("%Y%m%d-%H%M%S") + ".jpg"

template.save(filename)

# print it out!
os.system("lp -o portrait -o fit-to-page " + filename)