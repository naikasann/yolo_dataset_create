from types import ClassMethodDescriptorType
import xml.etree.ElementTree as ET
import os
from tqdm import tqdm
import pprint

def main():
    classes = ["mouse", "apple"]
    annotationfolder = "./Annotations"
    outputfolder = "./anotext"

    print("convert xml file to text file...")
    print("information.\n")

    print("=== classes ===")
    pprint.pprint(classes)
    print("===============\n")
    print("=== in & out ===")
    print("annotation folder : {}".format(annotationfolder))
    print("outputfolder      : {}".format(outputfolder))
    print("================\n")

    print("make output file.")
    os.makedirs(outputfolder, exist_ok=True)

    print("convert xml file 2 text. One moment, please...")
    files = os.listdir(annotationfolder)
    for file in tqdm(files):
        convert_annotation(classes, os.path.join(annotationfolder, file), outputfolder, file)
    print("\nok. pls check the outputfolder you have set!")

def convert(size, box):
    # Calculate the size ratio of the image (the whole image as 1)
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    # Calculate the perspective of the annotation box.
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    # Calculate the size of the box
    w = box[1] - box[0]
    h = box[3] - box[2]
    # Calculate and return the required annotation information.
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(classes, inputfile, outputfolder, output_filename):
    file = open(inputfile)

    tree=ET.parse(file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        with open(outputfolder + "/" + str(output_filename) + ".txt", mode="w") as writefile:
            writefile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    file.close()

if __name__ == "__main__":
    main()