import math
import cv2.cv as cv

loadPath = raw_input('Enter name of video: ')
runNum = str(raw_input('Enter Run number: '))
frameRate = int(raw_input('Enter Frame Rate: '))
cap = cv2.VideoCapture(loadPath+'.avi')


global boxes
global sbox
global ebox
boxes = []

def speedCalc(pt1, pt2, frameRate):
    dX = pt2[0] - pt1[0]
    dY = pt2[1] - pt1[1]
    
    try:
        speedVec = [dX/frameRate, dY/frameRate]
    except:
        speedVec = 0
    return speedVec
    
def angleCalc(pt1, pt2):
    dX = pt2[0]-pt1[0]
    dY = pt2[1]-pt1[1]
    angle = abs(math.atan2(dY, dX)*180/math.pi)
    return angle

def midCalc(pt1, pt2):
    dX = pt2[0] - pt1[0]
    dY = pt2[1] - pt1[1]
    
    midX = abs(pt1[0] + dX/2)
    midY = abs(pt1[1] + dY/2)
    
    return [midX, midY]
    
def on_mouse(event, x, y, flags, params):
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print 'Start Mouse Position: '+str(x)+', '+str(y)
        sbox = [x, y]
        boxes.append(sbox)
    elif event == cv.CV_EVENT_LBUTTONUP:
        print 'End Mouse Position: '+str(x)+', '+str(y)
        ebox = [x, y]
        boxes.append(ebox)

count = 0
while(1):
    count += 1
    _,img = cap.read()
    img = cv2.blur(img, (3,3))
    
    cv2.namedWindow('real image')
    cv.SetMouseCallback('real image', on_mouse, 0)
    cv2.imshow('real image', img)
        
    if count < 50:
        if cv2.waitKey(1) == 27:
            break
    elif count >= 50:
        if cv2.waitKey(0) == 27:
            break
        count = 0
cv2.destroyAllWindows()
cap.release()

boxes_sorted = zip(boxes,boxes[1:])[::2]
print boxes_sorted

angles = []
midpoints = []
for box in boxes_sorted:
    print box
    print box[0]
    print box[1]
    angle = angleCalc(box[0], box[1])
    angles.append(round(angle, 3))
    midpoint = midCalc(box[0], box[1])
    midpoints.append(midpoint)
    
data = []
for j in range(len(angles)):
    data.append((boxes_sorted[j], midpoints[j], angles[j]))
    
f = open(loadPath+runNum+' data out.txt', 'w')
f.write('Coords            | midpoint| angle\n')
for point in data:
    print point
    datastring = str(point)+'\n'
    datastring = datastring.strip('(').replace(')', '').replace('],', '|').replace('[', '')
    f.write(datastring)
f.close() 
