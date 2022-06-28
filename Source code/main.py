import numpy as np
import math
import time
import os
import cv2
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy import ndimage as ndi 
from numba import jit 
import SeamCarving as SC
from CreateMask import getMaskObject

def main():
    
    # Load original image
    img = cv2.imread(".\img-original\img-original-dog1.jpg")
    img1, img2, img_show = img.copy(), img.copy(), img.copy()
    
    # Get the object mask to be deleted
    print("Step one: Get the object mask to be deleted")
    mask = getMaskObject(img1)
    draw1 = mask[0]
    mask1 = mask[1]
    im_mask1_show = mask1.copy()
    print("Create Mask 1, DONE!!!")
    
    # Get the object mask to be protected
    print("Step two: Get the object mask to be protected")
    mask = getMaskObject(img2)
    draw2 = mask[0]
    mask2 = mask[1]
    im_mask2_show = mask2.copy()
    print("Create Mask 2, DONE!!!")
    
    h, w, c = img.shape
    originalImage = img.shape
    
    # Delete object
    start1 = time.time()
    img_pair = SC.removeObjectfromMask(img, mask2, mask1)
    img, img_mask_protected = img_pair[0], img_pair[1]
    img_removeObject_show = img.copy()
    end1 = time.time()
    
    # Save and revert object' size
    numberResult = math.ceil(len(os.listdir('./img-result')) / 3) + 1
    cv2.imwrite('.\img-result\img0' +  str(numberResult) + '-result.png', img)
    start2 = time.time()
    img_revert = revertSize((h, w, c), img, numberResult, img_mask_protected)
    end2 = time.time()
    
    # Create .gif file
    start3 = time.time()
    SC.produceVideo('.\img-gif\dynamicImage04.gif', originalImage)
    end3 = time.time()
    
    # Time consuming
    print(f"Time consuming in order to remove object use Seam Carving: {end1 - start1}s\n")
    print(f"Time consuming in order to revert image equal to original image's size: {end2 - start2}s\n")
    print(f"Time consuming in order to save video: {end3 - start3}s")
    
    
def revertSize(originalShape, curImage, numberResult, maskInsert):
    h, w, c = originalShape
    print(curImage.shape)
    hs, ws, cs = curImage.shape
    curImage = SC.enlargeImage(curImage, w - ws, maskInsert)
    cv2.imwrite('.\img-result\img0' +  str(numberResult) + '-final.png', curImage)
    return curImage
    
if __name__ == "__main__":
    main()
