# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 09:57:23 2013

@author: John
"""

import cv2, os
import numpy as np
from PIL import Image

def deleteFiles(dirPath):
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath+fileName)
        print '[-] File '+dirPath+fileName+' has been deleted'
    print '[*] All files in '+dirPath+' have been deleted'

loadPath = 'video.avi'
savePath = 'video_tracking_log.txt'


print 'Colour bounds in CV are half that of gimp...'
print 'Green = 60-80, Red = 140-180, Blue = 80-100, Yellow = 30-50'
lowerBound = int(raw_input('Enter lower colour bound (0-180): '))
upperBound = int(raw_input('Enter upper colour bound (0-180): '))

deleteFiles('out/')
deleteFiles('in/')
print '[*] out and in folders empty'
try:
    os.remove(savePath)
    print '[*] tracking log deleted'
except:
    print '[%] No tracking log present'

# create video capture
cap = cv2.VideoCapture(loadPath)
data = []
f = open(savePath, 'w')
count = 0
while(1):

    # read the frames
    _,frame = cap.read()

    # smooth it
    frame = cv2.blur(frame,(3,3))

    # convert to hsv and find range of colors
    try:
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    except(ValueError):
        print '[%] Incorrect hsv value.'
        f.close
        break
    except:
        print '[%] Unknown Error.'
        f.close
        break
        
    thresh = cv2.inRange(hsv,np.array((int(lowerBound), 80, 80)), np.array((int(upperBound), 255, 255)))
    thresh2 = thresh.copy()

    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # finding centroids of best_cnt and draw a circle there
    try:
        M = cv2.moments(best_cnt)
    except(NameError):
        print '[%] No pixels between chosen values in the picture'
        print '[i] Program stopped'
        exit()
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.circle(frame,(cx,cy),5,255,-1)
    #print 'frame=',count,'x=',cx,'y=',cy
    print '[+] Frame '+str(count)+' analysed'
    f.write(str(count)+' '+str(cx)+' '+str(cy)+'\n')
    values = str(count), str(cx), str(cy)
    data.append(values)

    # Show it, if key pressed is 'Esc', exit the loop
    cv2.imshow('frame',frame)
    cv2.imshow('thresh',thresh2)
    cv2.imwrite('in\\frame'+str(count)+'.jpeg', frame)
    count += 1
    if cv2.waitKey(33)== 27:
        f.close
        break

# Clean up everything before leaving

cv2.destroyAllWindows()
cap.release()
print '[*] Analysis finished'


#Start image alignment
imageFile = 'in/'
dataFile = 'video_tracking_log.txt'
runName = 'frame'
savePath = 'out/'

f=open(dataFile)
content = [line.rstrip('\n') for line in f]
f.close()

frameNums = []
xValues = []
yValues = []
for i in range(len(content)):
    splitCoords = content[i].split(' ')
    frameNums.append(int(splitCoords[0]))
    xValues.append(int(splitCoords[1]))
    yValues.append(int(splitCoords[2]))

print '[*] Coordinates split'


maxx = max(xValues)
minx = min(xValues)

maxy = max(yValues)
miny = min(yValues)

oscillRangex = maxx - minx
oscillRangey = maxy - miny

sample = Image.open(imageFile+runName+'0.jpeg')
w, h = sample.size
img_size = (w+oscillRangex, h+oscillRangey)

for i in range(len(content)):
    x=maxx-xValues[i]
    y=maxy-yValues[i]
    bg=Image.new(sample.mode, (img_size))
    openPath = imageFile+runName+str(i)+'.jpeg'
    img = Image.open(openPath)
    img.load()
    bg.paste(img, (x, y))
    bg.save(savePath+runName+str(i)+'.jpeg')
    print '[+] Image '+str(i)+' Saved...'
print '[*] Image Alignment Complete'
