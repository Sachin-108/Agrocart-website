import cv2
import numpy as np
import urllib.request

# Replace the IP address with your phone's IP address
url = 'http://192.0.0.4:8080/shot.jpg'

while True:
    # Use urllib to get the image from the IP Webcam server
    img_resp = urllib.request.urlopen(url)
    img_array = np.array(bytearray(img_resp.read()), dtype=np.uint8)
   
    # Decode the image array
    img = cv2.imdecode(img_array, -1)
   
    # Display the image
    cv2.imshow('Android Webcam', img)
   
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cv2.destroyAllWindows()