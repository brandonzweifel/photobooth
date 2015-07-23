from PIL import Image
import datetime
import os

# Load the template

os.chdir(os.path.dirname(os.path.realpath(__file__)))

template = Image.open("template-base.png")

# Create the composite
template.paste(Image.open("image1.jpg").resize((713, 536)), (175, 42))
template.paste(Image.open("image2.jpg").resize((713, 536)), (903, 42))
template.paste(Image.open("image3.jpg").resize((713, 536)), (175, 589))
template.paste(Image.open("image4.jpg").resize((713, 536)), (903, 589))

overlay = Image.open("template-overlay.png")

template.paste(overlay, (0, 0))

# Save it!
filename = os.path.dirname(os.path.realpath(__file__)) + "/archive/" + datetime.datetime.today().strftime("%Y%m%d-%H%M%S") + ".jpg"

template.save(filename)

# print it out!
os.system("lp " + filename)