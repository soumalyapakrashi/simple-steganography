import argparse
from PIL import Image
import numpy as np


def stringToBinary(message: str) -> str:
    output = ""
    for ch in message:
        value = (bin(ord(ch)).replace("0b", ""))
        
        padding = 8 - len(value)
        for i in range(padding):
            value = "0" + value
        
        output += value
    return output


def embedData(message: str, image):
    binary_message = stringToBinary(message)
    
    # Check if the given message will fit into the given image
    assert (len(binary_message) <= (image.shape[0] * image.shape[1])), "Given message is too big to fit in the given image"
    
    index = 0
    done = False
    for channel in range(image.shape[2]):
        for row in range(image.shape[0]):
            for column in range(image.shape[1]):
                if(index == len(binary_message)):
                    image[row][column][channel] = image[row][column][channel] | 1
                    done = True
                    break

                binary = binary_message[index]

                if(binary == "0"):
                    image[row][column][channel] = image[row][column][channel] & 254
                elif(binary == "1"):
                    image[row][column][channel] = image[row][column][channel] | 1

                index += 1

            if(done == True):
                break
        if(done == True):
            break
    
    return image


def extractEmbeddedData(image) -> str:
    bit_counter = 1
    bin_data = ""
    message = ""
    for channel in range(image.shape[2]):
        for row in range(image.shape[0]):
            for column in range(image.shape[1]):
                bin_data += str(image[row][column][channel] % 2)

                if(bit_counter % 8 == 0):
                    # Terminating condition
                    if(bin_data[0] == "1"):
                        return message
                    else:
                        message += chr(int(bin_data, 2))

                    # Reset the temporary variables
                    bin_data = ""

                bit_counter += 1


if(__name__ == "__main__"):
    # Setup arguments
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("operation", help = "The operation to perform - either embed or extract")
    argument_parser.add_argument("image", help = "Image on which to perform steganographic operation")
    argument_parser.add_argument("-m", "--message", help = "Message to embed")
    arguments = argument_parser.parse_args()

    image = Image.open(arguments.image)

    if(arguments.operation == "embed"):
        message = arguments.message
        assert (message != ""), "A message needs to be provided"
        img_array = np.array(image)
        embedded_image = embedData(message, img_array)
        new_image = Image.fromarray(embedded_image)
        new_image.save("output.png", compress_level = 0)
    
    elif(arguments.operation == "extract"):
        img_array = np.array(image)
        message = extractEmbeddedData(img_array)
        print(message)
    
    else:
        print("Invalid Operation")
    
    image.close()
