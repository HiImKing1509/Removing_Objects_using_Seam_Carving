import cv2
import numpy as np
from msvcrt import getch
import os
from numba import jit 

# mouse callback function
# drawing = False # true if mouse is pressed
# mode = True # if True, draw rectangle. Press 'm' to toggle to curve
# size_mouse = 10 
def getMaskObject(im):
    global drawing
    drawing = False
    global mode
    mode = True
    global size_mouse
    size_mouse = 10
    def maskDrawing(event,former_x,former_y,flags,param):
        global current_former_x,current_former_y,drawing, mode, size_mouse

        if event==cv2.EVENT_LBUTTONDOWN:
            drawing=True
            current_former_x,current_former_y=former_x,former_y

        elif event==cv2.EVENT_MOUSEMOVE:
            if drawing==True:
                if mode==True:
                    cv2.line(im,(current_former_x,current_former_y),(former_x,former_y),(0,0,0), size_mouse)
                    current_former_x = former_x
                    current_former_y = former_y
                    #print former_x,former_y
        elif event==cv2.EVENT_LBUTTONUP:
            drawing=False
            if mode==True:
                cv2.line(im,(current_former_x,current_former_y),(former_x,former_y),(0,0,0), size_mouse)
                current_former_x = former_x
                current_former_y = former_y
        return former_x,former_y    

    def createMask(img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cv2.imshow("Original image", img)
        # cv2.waitKey(0)

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j].all() == 0: img[i, j] = 255
                else: img[i, j] = 0
        return img

    cv2.namedWindow("Create Mask")
    cv2.setMouseCallback('Create Mask', maskDrawing)

    size_mouse = 10
    while(1):
        cv2.imshow('Create Mask', im)
        k=cv2.waitKey(1)&0xFF
        if k == 27: 
            img_draw = im.copy()
            break
        elif k == 105: 
            size_mouse += 2
            if size_mouse >= 100:
                size_mouse = 100
                print(f"Upper limit, Increase size mouse = {size_mouse}")
            else:
                print(f'Increate size mouse = {size_mouse}')
        elif k == 100:
            size_mouse -= 2
            if size_mouse < 2:
                size_mouse = 2
                print(f"Lower limit, Decrease size mouse = {size_mouse}")
            else:
                print(f'Decrease size mouse = {size_mouse}')
        elif k == 32:
            if size_mouse == 100:
                size_mouse = 2
                print(f'Decrease size mouse = {size_mouse}')
            elif size_mouse == 2:
                size_mouse = 50
                print(f'Increase size mouse = {size_mouse}')
            else:
                size_mouse = 100
                print(f'Increase size mouse = {size_mouse}')
    cv2.destroyAllWindows()

    return img_draw, createMask(im)