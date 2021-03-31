import os
import cv2
import numpy as np

class trafficSignal:
    def trafficLigh(img):
      #convert The frame to BGR to HSV
      font = cv2.FONT_HERSHEY_SIMPLEX
      cimg = img         #OpeCV  uses BRG insted of RGB . Conterted In to HSV
      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
      cv2.imshow("HSV",hsv)
      # color range
      lower_red1 = np.array([0,100,100])
      upper_red1 = np.array([10,255,255]) #For Red 
    
      lower_red2 = np.array([160,100,100])  
      upper_red2 = np.array([180,255,255])
    
      lower_green = np.array([40,50,50])    #Green 
      upper_green = np.array([90,255,255])
      
      lower_yellow = np.array([15,150,150]) #Yello
      upper_yellow = np.array([35,255,255])
    
      mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
      mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
      maskg = cv2.inRange(hsv, lower_green, upper_green)
      masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
      maskr = cv2.add(mask1, mask2)
      size = img.shape
      print(size,"Size Of The Signal Image Afer HSV")
    
      # hough circle detect
      r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80, param1=75, param2=5, minRadius=0, maxRadius=30)
      g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 60,param1=50, param2=10, minRadius=0, maxRadius=30)
      y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30,param1=50, param2=5, minRadius=0, maxRadius=30)
      # traffic light detect
      r = 5
      bound = 4.0 / 10
      if r_circles is not None:
        r_circles = np.uint16(np.around(r_circles))
    
        for i in r_circles[0, :]:
          if i[0] > size[1] or i[1] > size[0]or i[1] > size[0]*bound:
            continue
    
          h, s = 0.0, 0.0
          for m in range(-r, r):
            for n in range(-r, r):
    
              if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                continue
              h += maskr[i[1]+m, i[0]+n]
              s += 1
          red = h/s    
          if  red > 90:
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(maskr, (i[0], i[1]), i[2], (255, 255, 255), 2)
          
            cv2.putText(cimg,'RED',(i[0], i[1]), font, 1,(0,0,255),3,cv2.LINE_AA)
            
            print(red,end=" ")
        print("Red Value In Frame")
        Red,Green,Yello = (cimg[300, 300])
        print ("Red Block Yello",Yello)
        print ("Red block Green",Green)
        print ("Red block Red",Red )
    #For Green Signal pr Colour 
      elif g_circles is not None:
        
        g_circles = np.uint16(np.around(g_circles))
    
        for i in g_circles[0, :]:
          if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
            continue
    
          h, s = 0.0, 0.0
          for m in range(-r, r):
            for n in range(-r, r):
              if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                continue
              h += maskg[i[1]+m, i[0]+n]
              s += 1
          if h / s > 10:
            cv2.circle(cimg, (i[0], i[1]), i[2]+80, (0, 255, 0), 2)
            cv2.circle(maskg, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
            cv2.putText(cimg,'GREEN',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)
        
        print("--Green--")
        Red,Green,Yello = (cimg[300, 300])
        print ("Green Block Red",Red)
        print ("Green Block Green",Green)
        print ("Green Block yello",Yello )
      else :
        #for The Yellow/Orange Colour 
        print("Yellow")
        y_circles = np.uint16(np.around(y_circles))
        for i in y_circles[0, :]:
          if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
            continue
    
          h, s = 0.0, 0.0
          for m in range(-r, r):
            for n in range(-r, r):
              if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                continue
              h += masky[i[1]+m, i[0]+n]
              s += 1
          if h / s > 50:
            cv2.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
            cv2.circle(masky, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
            cv2.putText(cimg,'YELLOW',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)
        # distributed In The Different Colours
        Red,Green,Yello = (cimg[300, 300])
        print ("yellow Block Red == ",Red)
        print ("yellow Block Green===",Green)
        print ("yellow Block yellow====",Yello )
      cv2.imshow("Image",cimg)
      
      return Yello,Green,Red,cimg


    def Signalline(frame):
        #Red Signal Mark Line 
        cv2.line(frame,(0,270),(800,270),(0,255,0),1) # GreenLine
                
        cv2.line(frame,(0,290),(800,290),(0,0,255),3) # RedLine
        
        cv2.line(frame,(0,310),(800,310),(0,255,0),1) # GreenLine
        
#=-----------------------------------------------------------------------------
"""
imgpath="/home/sumeetgadewar/Downloads/Project eDBDA/Red.png"
font = cv2.FONT_HERSHEY_SIMPLEX
Limg = cv2.imread(imgpath) 
#Function CAll
Yello,Green,Red,frame = trafficSignal.trafficLigh(Limg)


if Red>Green and Red>Yello:
    print("red")
elif Green>Yello and Green>Red:
    print("Green")
else:
    print("Yello")
"""
#------------------------------------------------------------------------------    
""" 
#from The Automation File
    ### Red Light   ###################################################################
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    font = cv2.FONT_HERSHEY_SIMPLEX
    # color range
    lower_red1 = np.array([0,100,100])
    upper_red1 = np.array([10,255,255])

    lower_red2 = np.array([160,100,100])
    upper_red2 = np.array([180,255,255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80, param1=50, param2=10, minRadius=0, maxRadius=30)

    maskr = cv2.add(mask1, mask2)
    size = frame.shape
    # print size

    # hough circle detect
    r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80, param1=50, param2=10, minRadius=0, maxRadius=30)

     # traffic light detect
    r = 5
    bound = 4.0 / 10
    if r_circles is not None:
        r_circles = np.uint16(np.around(r_circles))

    for i in r_circles[0, :]:
        if i[0] > size[1] or i[1] > size[0]or i[1] > size[0]*bound:
            continue
    h, s = 0.0, 0.0
    for m in range(-r, r):
      for n in range(-r, r):

        if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
          continue
        h += maskr[i[1]+m, i[0]+n]
        s += 1
    if h / s > 50:
      cv2.circle(frame, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
      cv2.circle(maskr, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
      cv2.putText(frame,'RED',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)
    #################################################################################
"""