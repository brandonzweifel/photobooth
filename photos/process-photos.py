from PIL import Image
import datetime
import os

# Load the template

os.chdir(os.path.dirname(os.path.realpath(__file__)))

template = Image.open("template-base.png")

# Create the composite
template.paste(Image.open("image1.jpg").resize((713, 536)), (286, 58))
template.paste(Image.open("image2.jpg").resize((713, 536)), (1015, 58))
template.paste(Image.open("image3.jpg").resize((713, 536)), (286, 607))
template.paste(Image.open("image4.jpg").resize((713, 536)), (1015, 607))

# Save it!
filename = os.path.dirname(os.path.realpath(__file__)) + "/archive/" + datetime.datetime.today().strftime("%Y%m%d-%H%M%S") + ".jpg"

template.save(filename)
# template.save("output.jpg")

# print it out!
os.system("lp -o orientation-requested=5 " + filename)