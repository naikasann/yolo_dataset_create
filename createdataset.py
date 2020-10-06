"""
Training of yolo (Darknet) using dataset files exported by Pascal VOC from VoTT-annotated projects.
The program creates a dataset from a set of text files that contain the directory of the dataset.
input  : inputfiles => [A directory of text files for each category]
            foldername => [Folder name to be attached to the directories in (optional)]
            outputfile => Output text file name
output : A text file showing the location of the dataset used to train Yolo (Darknet)
"""
from tqdm import tqdm

############# input data set #############
inputfiles = ["testdata/apple_train.txt", "testdata/mouse_train.txt"]
foldername = "testdata/"
outputfile = "dataset.txt"
##########################################

outputdata = []
# Open the files of each class
print("============ input  data ============")
for inputfile in inputfiles:
    with open(inputfile, mode="r", encoding="utf-8") as loadfile:
        print("openfile : {}".format(inputfile))
        readline = loadfile.read().split("\n")
        print("Number of data : {}".format(len(readline)))
        for str in tqdm(readline):
            directory = str.split(" ")[0]
            # Removing Duplicates
            if not directory in outputdata:
                outputdata.append(directory)
print("The result of the output with the duplicates removed : {}".format(len(outputdata)))
print("=====================================")

print("============ output data ============")
print("Outputs a dataset for training Yolo using darknet....")
with open(outputfile, mode="w") as writefile:
    for data in tqdm(outputdata):
        writefile.writelines(foldername + data + "\n")
print("=====================================")