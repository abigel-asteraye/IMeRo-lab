import cv2
import csv
import pyrealsense2 as rs
import numpy as np
from realsense_depth import *
import os

# Creating a pipelines
pipe1= rs.pipeline()
pipe2= rs.pipeline()

# Creating a config objects and configuring the pipeline for each camera
cfg1= rs.config()
cfg1.enable_device('035322250133')
cfg1.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)
cfg1.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30 )

cfg2= rs.config()
cfg2.enable_device('035322250740')
cfg2.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)
cfg2.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30 )
# Starting the pipeline
pipe1.start(cfg1)
pipe2.start(cfg2)

# Create a folder to save the images
output_folder = 'images'
os.makedirs(output_folder, exist_ok=True)

# Creating a CSV file to save the captured image data
img_csv= open('captured_images.csv', 'w', newline='')
img_csv_writer= csv.writer(img_csv)


try:
    img_count=0 #Keeps track of the captured images
    while True and img_count < 10:
        #Wait for the nect set of frames
        frame_1= pipe1.wait_for_frames()
        frame_2= pipe2.wait_for_frames()

        #Getting the depth frame
        depth_frame1= frame_1.get_depth_frame()
        depth_frame2= frame_2.get_depth_frame()

        #Getting the color frame
        color_frame1= frame_1.get_color_frame()
        color_frame2= frame_2.get_color_frame()

        if not color_frame1 or not depth_frame1 or not color_frame2 or not depth_frame2:
            continue

        # Converting the frams to a numpy array
        depth_image1= np.asanyarray(depth_frame1.get_data())
        depth_image2= np.asanyarray(depth_frame2.get_data())

        color_image1= np.asanyarray(color_frame1.get_data())
        color_image2= np.asanyarray(color_frame2.get_data())

        # Saves the color image as a file
        img_count+=1
        col_img_filename1= f'c_image_1_{img_count}.jpg'
        image_path_1c = os.path.join(output_folder, col_img_filename1)

        col_img_filename2= f'c_image_2_{img_count}.jpg'
        image_path_2c= os.path.join(output_folder, col_img_filename2)


        depth_img_filename1= f'd_image_1_{img_count}.jpg'
        image_path_1d= os.path.join(output_folder, depth_img_filename1)

        depth_img_filename2= f'd_image_2_{img_count}.jpg'
        image_path_2d= os.path.join(output_folder, depth_img_filename2)


        cv2.imwrite(image_path_1c, color_image1)
        cv2.imwrite(image_path_2c, color_image2)

        cv2.imwrite(image_path_1d, depth_image1)
        cv2.imwrite(image_path_2d, depth_image2)

        ## Add the image names to a CSV file
        img_csv_writer.writerow([col_img_filename1, depth_img_filename1, col_img_filename2, depth_img_filename2])


finally:
    ## Closing the CSV and the pipelines
    img_csv.close()
    pipe1.stop()
    pipe2.stop()
