# USAGE
# python predict.py

# import the necessary packages
import config
import matplotlib.pyplot as plt
import numpy as np
import torch
import cv2
import os
def prepare_plot(origImage, origMask, predMask):
    # initialize our figure
    figure, ax = plt.subplots(nrows=1, ncols=3, figsize=(10, 10))
    
    # plot the original image, its mask, and the predicted mask
    ax[0].imshow(origImage)
    ax[1].imshow(origMask)
    ax[2].imshow(predMask)
    
    # set the titles of the subplots
    ax[0].set_title("Image")
    ax[1].set_title("Original Mask")
    ax[2].set_title("Predicted Mask")
    
    # set the layout of the figure and display it
    figure.tight_layout()
    plt.show()

def make_predictions(model, imagePath):
    # set model to evaluation mode
    model.eval()
    # turn off gradient tracking
    with torch.no_grad():
        # load the image from disk, swap its color channels, cast it
        # to float data type, and scale its pixel values
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype("float32") / 255.0
        # resize the image and make a copy of it for visualization
        image = cv2.resize(image, (config.INPUT_IMAGE_WIDTH, config.INPUT_IMAGE_HEIGHT))
        orig = image.copy()
        # find the filename and generate the path to the ground truth mask
        filename = imagePath.split(os.path.sep)[-1]
        groundTruthPath = os.path.join(config.MASK_DATASET_PATH, filename)

        # Load the ground-truth segmentation mask in grayscale mode and resize it
        gtMask = cv2.imread(groundTruthPath, cv2.IMREAD_GRAYSCALE)
        gtMask = cv2.resize(gtMask, (config.INPUT_IMAGE_WIDTH, config.INPUT_IMAGE_HEIGHT))

        # make the channel axis to be the leading one, add a batch
        # dimension, create a PyTorch tensor, and flash it to the
        # current device
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image, 0)
        image = torch.from_numpy(image).to(config.DEVICE)

        # make the prediction, pass the results through the sigmoid
        # function, and convert the result to a NumPy array
        predMask = model(image).squeeze()
        predMask = torch.sigmoid(predMask)
        predMask = predMask.cpu().numpy()

        # filter out the weak predictions and convert them to integers
        predMask = (predMask > config.THRESHOLD) * 255
        predMask = predMask.astype(np.uint8)

        # prepare a plot for visualization
        prepare_plot(orig, gtMask, predMask)

# load the image paths in our testing file and randomly select 10
# image paths
print("[INFO] Loading up test image paths...")
imagePaths = open(config.TEST_PATHS).read().strip().split("\n")
imagePaths = np.random.choice(imagePaths, size=10)

# load our model from disk and move it to the current device
print("[INFO] Loading the model...")
unet = torch.load(config.MODEL_PATH).to(config.DEVICE)

# iterate over the randomly selected test image paths
for path in imagePaths:
    # make predictions and visualize the results
    make_predictions(unet, path)


##new below

# import the necessary packages
import config
import matplotlib.pyplot as plt
import numpy as np
import torch
import cv2
import os

def prepare_plot(origImage, origMask, predMask, save_path=None):
    # initialize our figure
    figure, ax = plt.subplots(nrows=1, ncols=3, figsize=(10, 10))
    
    # plot the original image, its mask, and the predicted mask
    ax[0].imshow(origImage)
    ax[1].imshow(origMask)
    ax[2].imshow(predMask)
    
    # set the titles of the subplots
    ax[0].set_title("Image")
    ax[1].set_title("Original Mask")
    ax[2].set_title("Predicted Mask")
    
    # set the layout of the figure
    figure.tight_layout()
    
    if save_path:
        figure.savefig(save_path)
    else:
        plt.show()

def make_predictions(model, imagePath, save_path=None):
    # set model to evaluation mode
    model.eval()
    # turn off gradient tracking
    with torch.no_grad():
        # load the image from disk, swap its color channels, cast it
        # to float data type, and scale its pixel values
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype("float32") / 255.0
        # resize the image and make a copy of it for visualization
        image = cv2.resize(image, (config.INPUT_IMAGE_WIDTH, config.INPUT_IMAGE_HEIGHT))
        orig = image.copy()
        # find the filename and generate the path to the ground truth mask
        filename = imagePath.split(os.path.sep)[-1]
        groundTruthPath = os.path.join(config.MASK_DATASET_PATH, filename)

        # Load the ground-truth segmentation mask in grayscale mode and resize it
        gtMask = cv2.imread(groundTruthPath, cv2.IMREAD_GRAYSCALE)
        gtMask = cv2.resize(gtMask, (config.INPUT_IMAGE_WIDTH, config.INPUT_IMAGE_HEIGHT))

        # make the channel axis to be the leading one, add a batch
        # dimension, create a PyTorch tensor, and flash it to the
        # current device
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image, 0)
        image = torch.from_numpy(image).to(config.DEVICE)

        # make the prediction, pass the results through the sigmoid
        # function, and convert the result to a NumPy array
        predMask = model(image).squeeze()
        predMask = torch.sigmoid(predMask)
        predMask = predMask.cpu().numpy()

        # filter out the weak predictions and convert them to integers
        predMask = (predMask > config.THRESHOLD) * 255
        predMask = predMask.astype(np.uint8)

        # prepare a plot for visualization or save as an image
        prepare_plot(orig, gtMask, predMask, save_path)

# load the image paths in our testing file and randomly select 10
# image paths
print("[INFO] Loading up test image paths...")
imagePaths = open(config.TEST_PATHS).read().strip().split("\n")
imagePaths = np.random.choice(imagePaths, size=10)

# load our model from disk and move it to the current device
print("[INFO] Loading the model...")
unet = torch.load(config.MODEL_PATH).to(config.DEVICE)

# Create a directory for saving output figures
os.makedirs("output_figures", exist_ok=True)

# iterate over the randomly selected test image paths
for path in imagePaths:
    # Define a save path for the figures (optional)
    save_path = f"output_figures/{os.path.basename(path).split('.')[0]}_output.png"
    
    # make predictions and save the figures
    make_predictions(unet, path, save_path)
