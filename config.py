# import the necessary packages
import torch
import os

# base path of the dataset
DATASET_PATH = os.path.join("dataset", "train")

# define the path to the images and masks dataset
IMAGE_DATASET_PATH = os.path.join(DATASET_PATH, "images")
MASK_DATASET_PATH = os.path.join(DATASET_PATH, "masks")  # Adjust this path
#MASK_FILE_EXTENSION = "*.png"  # Define the file extension for mask files

# define the test split
TEST_SPLIT = 0.10

# determine the device to be used for training and evaluation
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# determine if we will be pinning memory during data loading
PIN_MEMORY = True if DEVICE == "cuda" else False

# define the number of channels in the input, number of classes,
# and number of levels in the U-Net model
NUM_CHANNELS = 2# Assuming RGB images, change this if you're using grayscale
NUM_CLASSES = 2  # You have two classes: "waterlevel" and "joints"
NUM_LEVELS = 3  # Adjust this as needed based on your specific architecture

# initialize learning rate, number of epochs to train for, and the batch size(batch size=64,num_epochs=40)
INIT_LR = 0.001
NUM_EPOCHS = 40
BATCH_SIZE = 64

# define the input image dimensions
# You should adapt the dimensions based on the majority resolution
# INPUT_IMAGE_WIDTH = 720(640,480)
INPUT_IMAGE_WIDTH = 128
INPUT_IMAGE_HEIGHT = 128

# define threshold to filter weak predictions
THRESHOLD = 0.5

# define the path to the base output directory
BASE_OUTPUT = "output"

# Update the following paths to handle multiple classes
MODEL_PATH = os.path.join(BASE_OUTPUT, "unet_your_model.pth")
PLOT_PATH = os.path.sep.join([BASE_OUTPUT, "plot.png"])
TEST_PATHS = os.path.sep.join([BASE_OUTPUT, "test_paths.txt"])
