# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import os.path
from os import path
print("Current Working Dir: ", os.getcwd())
## Read the MP4 File
video_path = "video/"
fg_path = "output/"
img_list = os.listdir(video_path)
print(img_list)

def resize_img(img, scale_percent):
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim)
    return resized

def contrast_brightness_image(src1, a, g):
    h, w, ch = src1.shape
    src2 = np.zeros([h, w, ch], src1.dtype)
    dst = cv2.addWeighted(src1, a, src2, 1-a, g)
    dst_temp = resize_img(dst, 0.3)
    src1 = resize_img(src1, 0.3)
    #cv2.imshow("con-bri-demo", dst_temp)
    #cv2.imshow("old", src1)

    #cv2.waitKey(0)
    return dst

def write_image(file_name, path_folder, name_str):
    if not path.exists(path_folder):
        os.mkdir(path_folder)
    cap = cv2.VideoCapture(file_name)
    
    if cap.isOpened() == False:
        print("Error opening video stream or file")
    else:
        print("Load file successfully!")

## Name for file

    step_skip = 5
    index = 0
    count = 0
    while cap.isOpened():
        ret, image = cap.read()
        remaining = count%step_skip
        count = count + 1

        if remaining:
            continue
        
        if not ret:
            print("Load video done!")
            break
        # create white image for background
        
        cv2.imwrite(path_folder + "/fg_" + str(index)+ "_" + name_str+ ".jpeg", image)

        image = contrast_brightness_image(image, 2.3, 0)#第一个1.2为对比度  第二个为亮度数值越大越亮
        
        result_cut = np.full_like(image, (255, 255, 255))
        # convert to hsv
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        #rgb = "#34552E"
        #bgr = [int(rgb[5:7], 16), int(rgb[3:5], 16), int(rgb[1:3], 16)]
        #hsv = list(cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0])
        # print("hsv:", hsv)
        
                
        
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # set lower and upper color limits
        #low_val = (0,60,0) #iphone value
        
        low_val = (0,40,0) #cannon value
        high_val = (255,255,255)
        

        #low_val = (36,40,55) #cannon value
        #high_val = (77,255,255)
        # Threshold the HSV image 
        mask = cv2.inRange(hsv, low_val,high_val)
        # remove noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=np.ones((8,8),dtype=np.uint8))
        # apply mask to original image
        img_masked = cv2.bitwise_and(image, image,mask=mask)
      
        
        
        
        # threshold using inRange
        

        #range1 = (20, 50, 0)
        #range2 = (255, 255, 255)
        
        #range1 = (20, 50, 0)
        #range2 = (255, 255, 255)
        #mask = cv2.inRange(hsv_image, range1, range2)
        
        ## apply morphology closing and opening to mask
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.merge([mask, mask, mask])
        mask_inv = 255 - mask
        
        img_masked = cv2.bitwise_and(image, mask)
        white_masked = cv2.bitwise_and(result_cut, mask_inv)
        result = cv2.add(img_masked, mask_inv)
        
        result_temp = result
        # cv2.namedWindow('displaymywindows', cv2.WINDOW_NORMAL)
        # cv2.imshow('displaymywindows', result)
        # cv2.waitKey(0)
        
        #closed = cv2.erode(result, None, iterations=4)
        result_temp = cv2.medianBlur(result_temp, 31)
        
        mask = np.where(result_temp[:, :, 0:3] != np.asarray([255, 255, 255]))
        
        
        # cv2.namedWindow('displaymywindows', cv2.WINDOW_NORMAL)
        # cv2.imshow('displaymywindows', result)
        # cv2.waitKey(0)
        
        #closed = cv2.erode(result, None, iterations=4)
        
        #mask = np.where(result[:, :, 0:3] != np.asarray([255, 255, 255]))
        
        #minx = min(mask[0])
        #maxx = max(mask[0])
        #miny = min(mask[1])
        #maxy = max(mask[1])
        minx = max(min(mask[0]) - 50, 1)
        maxx = min(max(mask[0]) + 50, image.shape[0])
        miny = max(min(mask[1]) - 50, 1)
        maxy = min(max(mask[1])+ 50, image.shape[1])
        
        #result_cut1 = np.zeros((maxx - minx + 1, maxy - miny + 1, 3))
        ##print(result_cut.shape)
        #result_cut1[:, :, :] = 255
        #result_cut1[mask[0] - minx, mask[1] - miny, :] = result[mask[0], mask[1], :]
        #result_cut1 = result_cut1.astype(int)
        result_cut = result[minx:maxx, miny:maxy]

        mask_s = np.where(result_cut[:, :, 0:3] != np.asarray([255, 255, 255]))
        minx_s = min(mask_s[0])
        maxx_s = max(mask_s[0])
        miny_s = min(mask_s[1])
        maxy_s = max(mask_s[1])
        
        result_cut_s = result_cut[minx_s:maxx_s, miny_s:maxy_s]
        
        
        cropped = image[minx:maxx, miny:maxy]  # (left, upper, right, lower)
        
        
        cv2.imwrite(path_folder + "/fg_" + str(index)+ "_" + name_str+ ".png", result_cut_s)
        #cv2.imwrite(path_folder + "/fg_" + str(index) + ".jpeg", result_cut1)

        #cv2.imwrite(path_folder + "/fg_" + str(index) + ".jpg", image)
        cv2.imwrite(path_folder + "/fg_" + str(index) + "_" + name_str + ".bmp", cropped)
        #cv2.imwrite(path_folder + "/fg_" + str(index) + ".bmp", cropped)

        #cv2.imshow("result_cut", result_cut)
        #cv2.imshow("Image", image_copy)
        index = index +1
        #cv2.waitKey(0)


        # Ref: https://stackoverflow.com/a/61962060
        # Ref: https://stackoverflow.com/questions/54723141/segmentation-problem-for-tomato-leaf-images-in-plantvillage-dataset
index_t = 1
total = len(img_list)
path_folder = os.path.join(fg_path, "test")
for name_str in img_list:
    file_name = video_path + name_str
    print(file_name)
    #path_folder = os.path.join(fg_path, name_str)
    print(name_str)
    print(index_t, " of " , total)
    write_image(file_name, path_folder, name_str)
    index_t = index_t + 1
    
