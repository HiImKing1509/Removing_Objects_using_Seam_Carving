from pickletools import uint8
import numpy as np
import cv2
from numba import jit 
from scipy import ndimage as ndi 
import imageio
from tqdm import tqdm
import matplotlib.pyplot as plt

frame = []

COLOR = np.array([0,0,255])

@jit
def genEnergyMap(img):
    """
        Use Canny Edge detection to generate Energy Map from image
    """
    Gx = ndi.convolve1d(img, np.array([1, 0, -1]), axis=1, mode='wrap')
    Gy = ndi.convolve1d(img, np.array([1, 0, -1]), axis=0, mode='wrap')
    energyMap = np.sum(Gx**2, axis=2) + np.sum(Gy**2, axis=2)
    return energyMap

@jit
def genSeamMap(energyMap):
    """
        Use Dynamic Programming to generate Seam Map from energy map
    """
    h, w = energyMap.shape 
    seamMap = energyMap.copy().astype(np.int64)
    for i in range(1, h):
        for j in range(0, w):
            seamMap[i, j] = 1e18
            for jj in range (-1,2,1):
                position = j + jj
                if position>=0 and position<=w-1:
                    seamMap[i,j]=min(seamMap[i,j],seamMap[i-1,position]+energyMap[i,j])
    return seamMap
@jit
def getSeamLine(energyMap):
    """
        Trace back with Dynamic Programming table
        Get SeamLine from energyMap
    """
    # Generate SeamMap using DP
    # ? what does this function do?
    seamMap = genSeamMap(energyMap)
    # Get Seam line
    seam = []
    h, w = seamMap.shape
    index = np.argmin(seamMap[h-1, :])
    seam.append(index)
    for i in range(h-2, -1, -1):
        for j in range (-1,2,1):
            position=index+j
            # print(i,seamMap[i+1,index],energyMap[i+1,index]+seamMap[i,position])
            if position>=0 and position<=w-1 and seamMap[i+1,index]==energyMap[i+1,index]+seamMap[i,position]:
                
                seam.append(position)
                index=position
                break
    return np.array(seam)[::-1]
@jit
def removeSeamLineImg(img, seam):
    """
        Remove SeamLine from an image
    """
    h, w, c = img.shape
    result = np.zeros(shape=(h, w-1, c))
    for i in range(0, h):
        # print(i,seam[i],w-1)
        result[i, :seam[i], :] = img[i, :seam[i], :]
        if seam[i] + 1 <= w - 1:
            result[i, seam[i]:, :] = img[i, seam[i] + 1:, :]
    result = result.astype(np.uint8)
    return result
@jit
def removeSeamLineMask(mask, seam):
    """
        Remove SeamLine from an image
    """
    h, w = mask.shape
    result = np.zeros(shape=(h, w-1))
    for i in range(0, h):
        result[i, :seam[i]] = mask[i, :seam[i]]
        if seam[i]+1<=w-1:
            result[i, seam[i]:] = mask[i, seam[i]+1:]
    result = result.astype(np.uint8)
    return result
@jit
def removeObjectfromMask(img, objectMaskProtect, objectMaskDelete):
    """
        Remove Object from image also keep some valuable object
    """
    global frame
    maskProtect = objectMaskProtect.copy()
    maskDelete = objectMaskDelete.copy()
    tmp = np.sum(maskDelete.T,axis = 1)
    lenObject = len(np.where(tmp!=0)[0])
    frame.append(img)
    for step in tqdm(range(lenObject)):
        energyMap=genEnergyMap(img).astype(np.int64)

        energyMap = np.where((maskProtect==255), 1e8, energyMap)
        energyMap = np.where((maskDelete==255), -1e8, energyMap)
        
        seam=getSeamLine(energyMap)
        
        # temp=visualizeSeam(img,seam)
        frame.append(visualizeSeam(img,seam))
        img = removeSeamLineImg(img,seam).copy()

        maskProtect=removeSeamLineMask(maskProtect,seam).copy()
        maskDelete=removeSeamLineMask(maskDelete,seam).copy()

    return img, maskProtect
@jit
def insertSeam(img,seam):
    """
        Insert a seam line into an image
    """
    h, w, c = img.shape 
    tmp = np.zeros(shape=(h, w+1, c))
    for i in range(0, h):
        tmp[i, :seam[i], :] = img[i, :seam[i], :]
        tmp[i, seam[i]+1:, :] = img[i, seam[i]:, :]
        if seam[i] == 0:
            tmp[i, seam[i], :] = img[i, seam[i]+1, :]
        elif seam[i] == w-1:
            tmp[i, seam[i], :] = img[i, seam[i]-1, :]
        else:
            tmp[i, seam[i], :] = (img[i, seam[i]-1, :].astype(np.int32) + img[i, seam[i]+1, :].astype(np.int32)) / 2
    tmp = tmp.astype(np.uint8)
    return tmp
@jit
def enlargeImage(img, size, maskInsert):
    """
        Enlarge Image according to size
    """
    global frame
    tmp = img.copy()
    bufferSeam = []
    
    for step in tqdm(range(size)):
        energyMap=genEnergyMap(tmp)
        energyMap[np.where(maskInsert==255)] = 1000
        seam=getSeamLine(energyMap)
        bufferSeam.append(seam)
        h, w = maskInsert.shape
        new_mask = np.zeros(shape=(h, w-1))
        for i in range(h):
            new_mask[i, :seam[i]] = maskInsert[i, :seam[i]]
            new_mask[i, seam[i]:] = maskInsert[i, seam[i]+1:]
        maskInsert = new_mask
        tmp = removeSeamLineImg(tmp,seam).copy()
        
    for step in tqdm(range(size)):
        seam = bufferSeam.pop(0)
        frame.append(visualizeSeam(img,seam))
        img = insertSeam(img,seam).copy()
        bufferSeam = shiftSeam(bufferSeam, seam).copy()
    return img


@jit
def shiftSeam(bufferSeam, seam):
    """
        Map coordinate according to size
    """
    newBuffer = []
    for sm in bufferSeam:
        sm[np.where(sm>=seam)] += 2 
        newBuffer.append(sm)
    return newBuffer  

# @jit
def updateSeam(bufferSeam, seam):
    """
        Map coordinate according to size
    """
    newBuffer = []
    for sm in bufferSeam:
        sm[np.where(sm>=seam)] += 1 
        newBuffer.append(sm)
    return newBuffer

@jit
def visualizeSeam(img, seam, color=COLOR):
    """
        Visualize SeamLine on an image
    """
    h, w, c = img.shape
    tmp = img.copy()
    for i in range(0, h):
        tmp[i, seam[i], :] = color
    tmp = tmp.astype(np.uint8)
    return tmp

@jit
def produceVideo(videoPath, originalShape):
    global frame
    h, w, c = originalShape
    results = [np.zeros(shape=(h, w, c)).astype(np.uint8)]
    for fr in tqdm(frame):
        part = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
        results.append(imageio.core.util.Array(part))
    imageio.mimsave(videoPath, results)   

# @jit
def drawPractice(img, num=100):
    record = []
    clone = img.copy()
    tmp = img.copy()
    for i in tqdm(range(num)):
        emap = genEnergyMap(clone)
        seam = getSeamLine(emap)
        record.append(seam)
        clone = removeSeamLineImg(clone, seam)
    for i in tqdm(range(num)):
        seam = record.pop(0)
        tmp = visualizeSeam(tmp, seam, color=COLOR)
        record = updateSeam(record, seam)
    return tmp