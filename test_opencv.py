import cv2
import os
import math

colorPad = []
target = 0
colors = ["Blanc", "Jaune", "Rouge", "Bleu", "Vert"]

'''
    Blanc = 0
    Jaune = 1
    Rouge = 2
    Bleu  = 3
    Vert  = 4
'''
def getColor(r, g, b):
    if r > 100 and g > 100 and b > 100:
        return 0
    elif r > 100 and g > 100:
        return 1
    elif r > b and r > g:
        return 2
    elif b > g and b > r:
        return 3
    elif g > b and g > r:
        return 4

def getRotation(coords):
    center = [(coords[0] + coords[4]) / 2,
                  (coords[1] + coords[5]) / 2]

    diffs = [coords[0] - coords[6], coords[1] - coords[7]]

    rotation = math.atan(diffs[0]/diffs[1]) * 180 / math.pi

    if (diffs[1] < 0):
        rotation += 180

    elif (diffs[0] < 0):
        rotation += 360

    return [center, rotation]

def findArucoMarkers(img, colorPad, target, markerSize=4, totalMarkers=250, draw=True):
    gray = img
    key = getattr(cv2.aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = cv2.aruco.Dictionary_get(key)
    arucoParam = cv2.aruco.DetectorParameters_create()
    bboxs, ids, rejected = cv2.aruco.detectMarkers(
        gray, arucoDict, parameters=arucoParam)

    if ids != None:
        target += 1
    else:
        angle = None
    
    for idPan in range(len(bboxs)):
        bb = bboxs[idPan]
        cv2.aruco.drawDetectedMarkers(img, [bb])
        center, angle = getRotation([bb[0][2][0], bb[0][2][1], bb[0][3][0], bb[0][3][1], bb[0][0][0], bb[0][0][1], bb[0][1][0], bb[0][1][1]])

        point1 = ([int((bb[0][0][0] + bb[0][1][0]) / 2), int((bb[0][0][1] + bb[0][1][1]) / 2)])
        point2 = ([int((bb[0][1][0] + bb[0][2][0]) / 2), int((bb[0][1][1] + bb[0][2][1]) / 2)])
        point3 = ([int((bb[0][2][0] + bb[0][3][0]) / 2), int((bb[0][2][1] + bb[0][3][1]) / 2)])
        point4 = ([int((bb[0][3][0] + bb[0][0][0]) / 2), int((bb[0][3][1] + bb[0][0][1]) / 2)])

        point1[0] = point1[0] + (point1[0] - int((bb[0][1][0] + bb[0][3][0]) / 2))
        point1[1] = point1[1] + (point1[1] - int((bb[0][1][1] + bb[0][3][1]) / 2))

        point2[0] = point2[0] + (point2[0] - int((bb[0][2][0] + bb[0][0][0]) / 2))
        point2[1] = point2[1] + (point2[1] - int((bb[0][2][1] + bb[0][0][1]) / 2))

        point3[0] = point3[0] + (point3[0] - int((bb[0][3][0] + bb[0][1][0]) / 2))
        point3[1] = point3[1] + (point3[1] - int((bb[0][3][1] + bb[0][1][1]) / 2))

        point4[0] = point4[0] + (point4[0] - int((bb[0][0][0] + bb[0][2][0]) / 2))
        point4[1] = point4[1] + (point4[1] - int((bb[0][0][1] + bb[0][2][1]) / 2))

        try:
            color1 = img[point1[1], point1[0]]
            color2 = img[point2[1], point2[0]]
            color3 = img[point3[1], point3[0]]
            color4 = img[point4[1], point4[0]]

            if len(colorPad) == 0:
                colorPad.append([0,0,0,0,0])
                colorPad.append([0,0,0,0,0])
                colorPad.append([0,0,0,0,0])
                colorPad.append([0,0,0,0,0])
            
            colorPad[0][getColor(color1[2], color1[1], color1[0])] += 1
            colorPad[1][getColor(color2[2], color2[1], color2[0])] += 1
            colorPad[2][getColor(color3[2], color3[1], color3[0])] += 1
            colorPad[3][getColor(color4[2], color4[1], color4[0])] += 1
        
        except:
            print('err')
            continue

        img = cv2.circle(img, point1, radius=1, color=(0, 0, 255), thickness=-1)
        img = cv2.circle(img, point2, radius=1, color=(0, 0, 255), thickness=-1)
        img = cv2.circle(img, point3, radius=1, color=(0, 0, 255), thickness=-1)
        img = cv2.circle(img, point4, radius=1, color=(0, 0, 255), thickness=-1)

    return img, colorPad, target, angle


cap = cv2.VideoCapture(1)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width, height)
while True:
    success, img = cap.read()
    img, colorPad, target, angle = findArucoMarkers(img, colorPad, target)

    if target >= 10:
        result = []
        for pad in colorPad:
            max_value = max(pad)
            max_index = pad.index(max_value)
            result.append(colors[max_index])
        print(result)
        print(['Nord', 'Est', 'Sud', 'Ouest'])
        print(angle)
        break

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()