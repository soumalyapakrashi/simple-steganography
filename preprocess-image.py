from PIL import Image
import argparse

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("image", help = "Image to preprocess")
arguments = argument_parser.parse_args()

image = Image.open(arguments.image)

original_dimensions = (image.width, image.height)

TARGET_DIM = 1000
# For pictures with equal height and width
if(original_dimensions[0] == original_dimensions[1]):
    factor = original_dimensions[0] // TARGET_DIM
    dimensions = (original_dimensions[0] // factor, original_dimensions[1] // factor)

# For pictures with more width than height
elif(original_dimensions[0] > original_dimensions[1]):
    factor = original_dimensions[0] // TARGET_DIM
    dimensions = (original_dimensions[0] // factor, original_dimensions[1] // factor)

# For pictures with more height than width
elif(original_dimensions[0] < original_dimensions[1]):
    factor = original_dimensions[1] // TARGET_DIM
    dimensions = (original_dimensions[0] // factor, original_dimensions[1] // factor)

image = image.resize(dimensions)

image.save("input.png", compress_level = 0)