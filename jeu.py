import cv2
import os
import podsController
import lightsController
# Others variables
colorPad = []
target = 0
colors = ["Blanc", "Jaune", "Rouge", "Bleu", "Vert"]

# All questions
questions = [{}, {}, {}, {}, {}]

# All pods
pods = [17]

# Data of teams
teams = [{"color": None, "points": 0}, {"color": None, "points": 0}, {"color": None, "points": 0}, {"color": None, "points": 0}]

# Game is started
game_started = True

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    if not game_started:
        pods = podsController.register(img, pods)
        if len(pods) == 12:
            game_started = True
    else:
        if teams[0]['color'] is None:
            detectedPods = podsController.detect(img)
            print(detectedPods)
            if len(detectedPods) == 1 and detectedPods[0] == pods[0]:
                img, colorPad, target, angle = podsController.colorPod(img, colorPad, target)

                if target >= 10:
                    result = []
                    for pad in colorPad:
                        max_value = max(pad)
                        max_index = pad.index(max_value)
                        result.append(colors[max_index])
                    lightsController.padColor(angle, result)
                    print('Start lumière pod couleur')
                    teams[0]['color'] = result[0]
                    teams[1]['color'] = result[1]
                    teams[2]['color'] = result[2]
                    teams[3]['color'] = result[3]
                    print(result)
                    print(angle)
                    print(teams)
        else:
            print('Distribution des jetons aux joueurs')

    
    

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()