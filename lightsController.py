from laumio import Laumio
from presetIP import *
import random
import time

########## FONCTION TECHNIQUE ##########
def getCouleur(couleur):
	if(couleur == "Rouge"):
		return rouge
	if(couleur == "Blanc"):
		return blanc
	if(couleur == "Jaune"):
		return jaune
	if(couleur == "Bleu"):
		return bleu
	if(couleur == "Vert"):
		return vert
def padColor(angle, couleur):
	stop()
	if(angle>315 or angle < 45):
		print(angle)
		print("-- " + str(getCouleur(couleur[0])))
		listeLumiere = lumiere(ouestT)
		fillColorL(listeLumiere,100, getCouleur(couleur[0]))
		listeLumiere = lumiere(nord)
		fillColorL(listeLumiere, 100, getCouleur(couleur[1]))
		listeLumiere = lumiere(estT)
		fillColorL(listeLumiere, 100, getCouleur(couleur[2]))
		listeLumiere = lumiere(sud)
		fillColorL(listeLumiere, 100, getCouleur(couleur[3]))
	elif(angle > 45 and angle < 135):
		listeLumiere = lumiere(ouestT)
		fillColorL(listeLumiere, 100, getCouleur(couleur[3]))
		listeLumiere = lumiere(nord)
		fillColorL(listeLumiere, 100, getCouleur(couleur[0]))
		listeLumiere = lumiere(estT)
		fillColorL(listeLumiere, 100, getCouleur(couleur[1]))
		listeLumiere = lumiere(sud)
		fillColorL(listeLumiere, 100, getCouleur(couleur[2]))
	elif(angle > 135 and angle < 225):
		listeLumiere = lumiere(ouestT)
		fillColorL(listeLumiere, 100, getCouleur(couleur[2]))
		listeLumiere = lumiere(nord)
		fillColorL(listeLumiere, 100, getCouleur(couleur[3]))
		listeLumiere = lumiere(estT)
		fillColorL(listeLumiere, 100, getCouleur(couleur[0]))
		listeLumiere = lumiere(sud)
		fillColorL(listeLumiere, 100, getCouleur(couleur[1]))
	else:
		listeLumiere = lumiere(ouestT)
		fillColorL(listeLumiere, 100, getCouleur(couleur[3]))
		listeLumiere = lumiere(nord)
		fillColorL(listeLumiere, 100, getCouleur(couleur[0]))
		listeLumiere = lumiere(estT)
		fillColorL(listeLumiere, 100, getCouleur(couleur[1]))
		listeLumiere = lumiere(sud)
		fillColorL(listeLumiere, 100, getCouleur(couleur[2]))


def stop():
	for port in projecteurPort:
		Laumio("192.168.1.20").fillColorProjecteur(port,noir)
	listeLumiere = lumiere(tout)
	for lumiere in listeLumiere:
		lumiere.wipeOut()
def positionPourcentage(position, resolution):

	pourcentageSud = (position[1]*100/resolution[1])
	pourcentageNord = 1 - pourcentageSud

	pourcentageOuest = (position[0]*100/resolution[0])
	pourcentageEst = 1 - pourcentageOuest

	return [pourcentageNord,pourcentageEst,pourcentageSud,pourcentageOuest]

def calculPourcentage(pourcentage, rgb):
	return round((pourcentage * rgb[0]) / 100),round((pourcentage * rgb[1]) / 100),round((pourcentage * rgb[2]) / 100)

def lumiere(listeIp):
	tmp = []
	print(listeIp)
	for ip in listeIp:

		tmp.append(Laumio(ip))
	return tmp

########## FONCTION DE BASE AVEC LISTE ##########

def stop():
	for lumiere in listeLumiere:
		lumiere.wipeOut()

def fillColorL(listeLumiere, pourcentage, rgb):
	rgb = calculPourcentage(pourcentage, rgb)
	for lumiere in listeLumiere:
		lumiere.fillColor(rgb)

def fillRingL(listeLumiere, ringid, pourcentage, rgb):
	rgb = calculPourcentage(pourcentage, rgb)
	print(rgb)
	for lumiere in listeLumiere:
		lumiere.fillRing(ringid, rgb)

def fillColumnL(listeLumiere, columnid, pourcentage, rgb):
	rgb = calculPourcentage(pourcentage, rgb)
	for lumiere in listeLumiere:
		lumiere.fillColumn(columnid, rgb)

def setPixelColorL(listeLumiere, pixel, pourcentage, rgb):
	rgb = calculPourcentage(pourcentage, rgb)
	for lumiere in listeLumiere:
		lumiere.setPixelColor(pixel, rgb)

def colorWipeL(listeLumiere, delay, pourcentage, rgb):
	rgb = calculPourcentage(pourcentage, rgb)
	for lumiere in listeLumiere:
		lumiere.colorWipe(rgb, delay)

####### FONCTION ANIMATION ##########

# fonction clignoter led de bas en haut delay en seconde
def basHautL(listeLumiere, delay, rgb):
	for i in range(4):
		fillRingL(listeLumiere, i, 100, rgb)
		time.sleep(delay)
		fillRingL(listeLumiere, i, 100, rgb)

# fonction clignoter led de gauche a droite delay en seconde
def gaucheDroiteL(listeLumiere, delay, rgb):
	for i in range(3):
		fillColumnL(listeLumiere, i, 100, rgb)
		time.sleep(delay)
		fillColumnL(listeLumiere, i, 100, rgb)

def debarquement(listeLumiere, duree, rgb):
	stop()
	projecteur = Laumio("192.168.1.20")
	listePixel = []
	listePixel.append([2,3,8,10])
	listePixel.append([1,4,7,11])
	listePixel.append([0,5,6,12])
	listeLumiereAleatoire = []
	tempsTotal = 0

	while(True):
		nombreLumiereAleatoire = random.randint(5,len(listeLumiere)-1)
		for i in range(nombreLumiereAleatoire):
			lumiereAleatoire = random.randint(0,len(listeLumiere)-1)
			canalAleatoire = random.randint(0,3)
			listeLumiereAleatoire.append([lumiereAleatoire,canalAleatoire])

		for i in range(3):
			for lumiereAleatoire in listeLumiereAleatoire:
				listeLumiere[lumiereAleatoire[0]].wipeOut()
				listeLumiere[lumiereAleatoire[0]].setPixelColor(listePixel[i][lumiereAleatoire[1]], rgb)	
			time.sleep(0.15)
			tempsTotal+=0.15
		stop()


		if(random.randint(0,3)):
			for port in projecteurPort:
				print(port)
				projecteur.fillColorProjecteur(port,blanc)
			temps = random.randint(2,5)/10

		else:
			temps = random.randint(5,10)/10
		
		
		time.sleep(temps)
		for port in projecteurPort:
			projecteur.fillColorProjecteur(port,noir)
		tempsTotal+=temps
		listeLumiereAleatoire = []

		if(tempsTotal >= duree):
			break

def mer(listeLumiere, duree, vitesse, rgb):
	
	tempsTotal = 0
	i = 0
	while(True):
		stop()
		fillColorL(listeLumiere,10,rgb)
		if(i == 0):
			fillColorL([listeLumiere[9]],50,rgb)
			fillColorL([listeLumiere[0]],100,rgb)
			fillColorL([listeLumiere[1]],50,rgb)
		else:
			fillColorL([listeLumiere[i-1]],50,rgb)
			fillColorL([listeLumiere[i]],100,rgb)
			fillColorL([listeLumiere[i+1]],50,rgb)	
		print(rgb)
		i += 1
		if(i==len(listeLumiere)-1):
			i = 0
		time.sleep(vitesse)
		tempsTotal+=vitesse
		if(tempsTotal >= duree):
			break

def feu(listeLumiere, duree):
	tempsTotal = 0
	listePourcentage = [0,0,0]
	stop()
	fillRingL(listeLumiere,0,60,rouge)
	fillRingL(listeLumiere,1,80,orange)
	fillRingL(listeLumiere,2,100,jaune)
	listePourcentage[0] = 100
	listePourcentage[1] = 100
	listePourcentage[2] = 100


	while(True):
		listePourcentage[0] = random.randint(70,100)
		listePourcentage[1] = random.randint(70,100)
		listePourcentage[2] = random.randint(70,100)
		fillRingL(listeLumiere,0,listePourcentage[0],rouge)
		fillRingL(listeLumiere,1,listePourcentage[1],orange)
		fillRingL(listeLumiere,2,listePourcentage[2],jaune)
		
		tmp = random.randint(4,8)/10
		time.sleep(tmp)
		tempsTotal += tmp
		if(tempsTotal >= duree):
			break

def foret(listeLumiere, duree):
	projecteur = Laumio("192.168.1.20")
	for port in projecteurPort:
		projecteur.fillColorProjecteur(port,marron)
	tempsTotal = 0
	listePourcentage = [0,0,0]
	stop()
	fillRingL(listeLumiere,0,60,vertFonce)
	fillRingL(listeLumiere,1,80,vert)
	fillRingL(listeLumiere,2,100,bleuClaire)
	listePourcentage[0] = 100
	listePourcentage[1] = 100
	listePourcentage[2] = 100


	while(True):
		listePourcentage[0] = random.randint(80,100)
		listePourcentage[1] = random.randint(50,100)
		listePourcentage[2] = random.randint(70,100)
		fillRingL(listeLumiere,0,listePourcentage[0],vertFonce)
		fillRingL(listeLumiere,1,listePourcentage[1],vert)
		fillRingL(listeLumiere,2,listePourcentage[2],vert)
		
		tmp = random.randint(4,8)/10
		time.sleep(tmp)
		tempsTotal += tmp
		if(tempsTotal >= duree):
			break

def starWars(listeLumiere, duree):
	stop()
	tempsTotal = 0

	for i in range(9):
		listeLumiere[i].fillRing(2, rouge)
		if(i-1 >= 0):
			listeLumiere[i-1].wipeOut()
		time.sleep(0.2)
		tempsTotal += 0.2
	for i in range(8,-1,-1):
		listeLumiere[i].fillRing(2, vert)
		if(i+1 <= 8):
			listeLumiere[i+1].wipeOut()
		time.sleep(0.2)
		tempsTotal += 0.2

	for i in range(3):
		listeLumiere[1].fillRing(i, vert)
		listeLumiere[7].fillRing(i, rouge)
		time.sleep(0.4)







listeLumiere = lumiere(tout)

stop()

#mer(listeLumiere,18,0.6,bleu)
#debarquement(listeLumiere,10,bleu)
#feu(listeLumiere,10)
#foret(listeLumiere,10)
#starWars(listeLumiere,10)