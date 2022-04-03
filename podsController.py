import cv2
import os
import math

def register(img, pods):
    gray = img
    key = getattr(cv2.aruco, 'DICT_4X4_250')
    arucoDict = cv2.aruco.Dictionary_get(key)
    arucoParam = cv2.aruco.DetectorParameters_create()
    bboxs, ids, rejected = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)

    if ids != None and len(ids) == 1 and ids[0][0] not in pods:
        if len(pods) == 0:
            print("Enregistrement du pod couleur")
            pods.append(ids[0][0])
        elif len(pods) <= 1 or len(pods) > 4:
            print("Enregistrement du pod equipe")
            pods.append(ids[0][0])
        elif len(pods) <= 5 or len(pods) > 9:
            print("Enregistrement du pod question")
            pods.append(ids[0][0])
        elif len(pods) == 10:
            print("Enregistrement du pod valdier")
            pods.append(ids[0][0])
        elif len(pods) == 11:
            print("Enregistrement du pod pas valdier")
            pods.append(ids[0][0])
    return pods

def detect(img): 
    gray = img
    key = getattr(cv2.aruco, 'DICT_4X4_250')
    arucoDict = cv2.aruco.Dictionary_get(key)
    arucoParam = cv2.aruco.DetectorParameters_create()
    bboxs, ids, rejected = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)

    result = []

    if len(bboxs) > 0:
        for pod in ids:
            result.append(pod[0])
    return result

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

def colorPod(img, colorPad, target):
    gray = img
    key = getattr(cv2.aruco, 'DICT_4X4_250')
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

