#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 23:19:56 2021

@author: sumeetgadewar
"""
#--------------------------------------------------------------------------
#   An automatic traffic red-light violation detection system , 
#   which may play a big role in transportation management in smart cities. 
#   The system mainly relies on modern computer vision techniques, 
#   which was implemented in OpenCV under Python environment. 

#------------------------------------------------------------------------------
#"""
import cv2
from tracker import *
from trafficSignal import *

#=-----------------------------------------------------------------------------


# Create tracker object
tracker = EuclideanDistTracker()

sourc="/home/sumeetgadewar/Downloads/Project eDBDA/Final Code /Video/aziz1.mp4"
cap = cv2.VideoCapture(sourc)

# Object detection from Stable camera.
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
Vehical_count=0
option=input("Enter the Option to Select Using Training( T ) Set Or Masking( M ):- ")
if option=="M" or option=="m" :
    try:
        while True:
        #=-----------------------------------------------------------------------------
        #Function CAll
        
            ret, frm = cap.read()  #converted Into frame 
                
            height, width, _ = frm.shape # seprated To The Height and The Weight
            print(frm.shape[1],"width",frm.shape[0],"Hight")
                
            # Frame Resize with The STD 
            frames = cv2.resize(frm, (780, 640),interpolation = cv2.INTER_NEAREST)
        #-------------------------------------------------------------
            #Traffic Signal Light       TrafficLight Function 
               
            Yello,Green,Red,frame = trafficSignal.trafficLigh(frames)
        #----------------------------------------------------------------
        #----------------------------------------------------------------            
            finalframe=0
            #Condition For The Signal 
            if Red>Green and Red>Yello and Red > 30: 
                
                print("Value Of Red in Signal > ",Red,"-")
                        
     
                # Extract Region of interest// Signal Cross //walkWay // Xebra Crossing
                global roi
                roi = frame[230:270,100:800]
                
                #Traffic Line Function
                trafficSignal.Signalline(frame) 
                
                # 1. Object Detection
                mask = object_detector.apply(roi)
                    
                # Image Thresholding 
                """
      In this method, the pixel values of a grayscale image are assigned one of the 
      two values representing black and white colors based on a threshold. So, 
      if the value of a pixel is greater than a threshold value, it is assigned one value, 
      else it is assigned the other value."""                
                    # Thresholding on the output image of the previous step
                _, mask = cv2.threshold(mask, 30, 255, cv2.THRESH_BINARY)
                
                    # Perform image dilation on the output image of the previous step
                kernel = np.ones((3,3),np.uint8)        #Truck Problem Found 2 Object detect for a Truck  
                dilated = cv2.dilate(mask,kernel,iterations = 1)
                
                contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                detections = []
                for cnt in contours:   #Bounging The Area 
                    # Calculate area and remove small elements
                    area = cv2.contourArea(cnt)
                    
                    if area > 900:
                        #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 3)   
                        
                        #append the Detection Count
                        detections.append([x, y, w, h])
                print(len(detections),"Length of The detection ")
            
                # 2. Object Tracking    # EuclideanDistTracker Formula 
                boxes_ids = tracker.update(detections)
                for box_id in boxes_ids:
                    x, y, w, h, id = box_id
                    #cv2.putText(roi, ("Violation"+str(id)), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    
                    
                    #count The Vechical 
                    if x<205 and x>195:
                        Vehical_count = Vehical_count + 1
                    
                cv2.putText(frame,"Vehical Count:{}".format(Vehical_count), (150,20),cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0),2)
    
                    
                    #xMid = int((x+(x+w))/2)
                    #yMid = int((y+(y+h))/2)
                    #cv2.circle(roi,(xMid,yMid),5,(0,0,200),2)
                finalframe=frame    
                print(frame,"Processed Frame",frm,"Direct Frame")    
                cv2.imshow("Mask", mask)
                cv2.rectangle(frame, (170,10), (650,50), (255,255,255),-1)
                cv2.putText(frame,"Traffic Violation Count:{}".format(len(detections)), (200,40),cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255),2)
                cv2.putText(frame, ("Violation"+str(id)), (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                print(id)
                cv2.imshow("Video _ Frames", frame)
                cv2.imshow("roi", roi)
                cv2.imshow("dilated",dilated)
            else:
                finalframe=frame
        #cv2.imshow("Mask", mask)
                    
            cv2.imshow("Final and Only Final Frame", finalframe)
            key = cv2.waitKey(30)
            if key == 27:
                break
           
        cap.release()
        cv2.destroyAllWindows()  
    except:
        print("----Video Ends---")        
        #------------------------------------------------------------------------------
elif option=="T" or option=="t":    
    #load The HarCascade file 
    cascade_src="/home/sumeetgadewar/Downloads/Project eDBDA/CasCade FilrXML/cars3.xml"

    car_cascade=cv2.CascadeClassifier(cascade_src)
    while True:
        ret, frm = cap.read()
        frames = cv2.resize(frm, (780, 640),interpolation = cv2.INTER_NEAREST)
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        
        #global roi
        roi = frames[230:305,100:800]
        mask = object_detector.apply(roi)
        
       
        #-------------------------------------------
        #Traffic Line Function
        trafficSignal.Signalline(frames)
        
        # Calling The Cascade File 
        cars = car_cascade.detectMultiScale(roi, 1.1,1)
        for (x, y, w, h) in cars:
                                            #(Wedight,Hight)
            cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 0, 255), 2)  #Rectangle Bounding Box
        cv2.imshow("CasCade Roi",roi)
        cv2.imshow('sKSama', frames )
        if cv2.waitKey(30) == 27:
            break
    
    # De-allocate any associated memory usage
    cv2.destroyAllWindows()

else:
    print("Enter The Valid Option")
