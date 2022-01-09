import cv2
import time
import numpy as np
from cnn_model import *

def apply_taocyfff_filters(face_points, image_copy_1, image_name):

    '''
    Apply The Application Of Changing Your Face For Fun Filters to our faces

    Parameters:
    --------------
    face_points: The predicted facial keypoints from the camera
    image_copy_1: Copy of original image

    Returns:
    ---------------
    image_copy_1:
    
    '''

    taocyfff_filter = cv2.imread("images/"+image_name, cv2.IMREAD_UNCHANGED)

    for t in range(len(face_points)):
        # Get the width of filter depending on left and right eyebrow point
        # Adjust the size of the filter point to be positionally above the actual facial point
        filter_width = 1.1*(face_points[t][14]+15 - face_points[t][18]+15)
        scale_factor = filter_width/taocyfff_filter.shape[1]
        sg = cv2.resize(taocyfff_filter, None, fx=scale_factor, fy = scale_factor, interpolation=cv2.INTER_AREA)

        width = sg.shape[1]
        height = sg.shape[0]

        # top left corner of taocyfff_filter: x coordinate = average x coordinate of eyes - width/2
        # y coordinate = average y coordinate of eyes - height/2
        x1 = int((face_points[t][2]+5 + face_points[t][0]+5)/2 - width/2)
        x2 = x1 + width

        y1 = int((face_points[t][2]+5 + face_points[t][1]-65)/2 - height/3)
        y2 = y1 + height

        # Create a prime mask based on the transparency values
        prime_fill = np.expand_dims(sg[:, :, 3]/255.0, axis=-1)
        prime_face = 1.0 - prime_fill

        # Take a weighted sum of the image and the taocyfff filter using the prime values and (1- prime)
        image_copy_1[y1:y2, x1:x2] = (prime_fill * sg[:, :, :3] + prime_face * image_copy_1[y1:y2, x1:x2])

    return image_copy_1

# Load the model built in the previous steps
model = load_model('models/final_model')

# Get the frontal face har cascade
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

# Get the webcam
camera = cv2.VideoCapture(0)

while True:
    # Read data from the webcam
    _, image = camera.read()
    image_copy = np.copy(image)
    image_copy_1 = np.copy(image)
    image_copy_2 = np.copy(image)

    # Convery RGB image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Identify the faces in thewebcam using Haar cascades
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces_keypoints = []

    # Loop through faces
    for (x,y,w,h) in faces:

        # Crop whitespace
        face = gray[y:y+h, x:x+w]

        # Scale Face to 96 by 96
        scaled_face = cv2.resize(face, (96, 96), 0, 0, interpolation=cv2.INTER_AREA)

        # Normalize images to be between 0 and 1
        input_image = scaled_face / 255

        # Format image to be the correct shape for the model
        input_image = np.expand_dims(input_image, axis = 0)
        input_image = np.expand_dims(input_image, axis = -1)

        # Use model to predict keypoints on image
        face_points = model.predict(input_image)[0]

        # Adjust keypoint to coordinates of original image
        face_points[0::2] = face_points[0::2] * w/2 + w/2 + x
        face_points[1::2] = face_points[1::2] * h/2 + h/2 + y
        faces_keypoints.append(face_points)

        # Plot facial keypoints on image
        for point in range(15):
            cv2.circle(image_copy, (face_points[2*point], face_points[2*point + 1]), 2, (255, 255, 0), -1)

        sunglasses = apply_taocyfff_filters(faces_keypoints, image_copy_1, "sunglasses.png")
        sunKing_wig = apply_taocyfff_filters(faces_keypoints, image_copy_2,"victorian_costume.png")

        # Screen with the filter
        cv2.imshow('Screen with filter',sunglasses)
        cv2.imshow('Screen with filter frenchWig',sunKing_wig)

        #Screen with facial keypoints
        cv2.imshow('Screen with facial Keypoints predicted',image_copy)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break