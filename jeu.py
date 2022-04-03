import cv2
import os
import podsController
import lightsController
# Others variables
colorPad = []
target = 0
colors = ["Blanc", "Jaune", "Rouge", "Bleu", "Vert"]

startQuestion = 0

# All questions
questions = [{"finish": False, "start": False}, {"finish": False, "start": False}, {"finish": False, "start": False}, {"finish": False, "start": False}, {"finish": False, "start": False}]

# All pods
pods = []

# Data of teams
teams = [{"color": None, "points": 0}, {"color": None, "points": 0}, {"color": None, "points": 0}, {"color": None, "points": 0}]

# Game is started
game_started = False

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
            else:
                print("En attente du pod couleur")
        else:
            detectedPods = podsController.detect(img)
            if len(detectedPods) == 6 and pods[1] in detectedPods and pods[2] in detectedPods and pods[3] in detectedPods and pods[4] in detectedPods and pods[10] in detectedPods and pods[11] in detectedPods:
                if questions[startQuestion]["start"] and not questions[startQuestion]["finish"]:
                    print('rr')
                elif questions[startQuestion]["start"] and questions[startQuestion]["finish"]:
                    startQuestion += 1
                else: 
                    print('Dans le else')
            elif len(detectedPods) < 6 :
                if pods[1] in detectedPods and pods[2] in detectedPods and pods[3] in detectedPods and pods[4] in detectedPods:
                    if pods[10] in detectedPods:
                        print('Non validé')
                    else:
                        print('validé')
                else:
                    if pods[1] not in detectedPods:
                        print('Parole Equipe 1')
                    if pods[2] not in detectedPods:
                        print('Parole Equipe 2')
                    if pods[3] not in detectedPods:
                        print('Parole Equipe 3')
                    if pods[4] not in detectedPods:
                        print('Parole Equipe 4')

    
    

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()