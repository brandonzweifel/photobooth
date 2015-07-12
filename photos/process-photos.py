from PIL import Image
import datetime
import os

# Load the template

os.chdir(os.path.dirname(os.path.realpath(__file__)))

template = Image.open("template.png")

# Create the composite
template.paste(Image.open("image1.jpg").resize((559, 419)), (28, 468))
template.paste(Image.open("image2.jpg").resize((559, 419)), (609, 468))
template.paste(Image.open("image3.jpg").resize((559, 419)), (28, 912))
template.paste(Image.open("image4.jpg").resize((559, 419)), (609, 912))

# Save it!
filename = os.path.dirname(os.path.realpath(__file__)) + "/archive/" + datetime.datetime.today().strftime("%Y%m%d-%H%M%S") + ".jpg"

template.save(filename)

# print it out!
os.system("lp -o portrait " + filename)