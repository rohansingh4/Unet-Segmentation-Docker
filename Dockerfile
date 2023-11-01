# # Use an official Python 3.10 runtime as a parent image
# FROM python:3.10

# # Set the working directory to /app
# WORKDIR /app

# # Copy the contents of the current directory into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

# # Install libgl1-mesa-glx to resolve the libGL.so.1 issue
# RUN apt-get update && apt-get install -y libgl1-mesa-glx

# # Define environment variable
# ENV NAME World

# # Run your application
# CMD ["python", "predict.py"]





############# iteration 2

# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of your local codebase to the container
COPY . /app

# Install the required Python packages using pip
RUN pip install torch opencv-python matplotlib numpy scikit-learn tqdm imutils torchvision

# Expose a port if your application listens on a specific port
# EXPOSE 8080  # Uncomment this line if needed

# Define the command to run your Python script
CMD ["python", "predict.py"]


##############Iteration 3                  

# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of your local codebase to the container
COPY . /app

# Install the required Python packages using pip
RUN pip install torch opencv-python matplotlib numpy scikit-learn tqdm imutils torchvision

# Install the missing library
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Expose a port if your application listens on a specific port
# EXPOSE 8080  # Uncomment this line if needed

# Define the command to run your Python script
CMD ["python", "predict.py"]
