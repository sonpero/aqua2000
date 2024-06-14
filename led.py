#import libraries
import RPi.GPIO as GPIO
import time

#Initialisation
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#On utilise une variable avec le numéro du PIN
#Si vous avez suivi mes images, c'est le port 7 => BCM 4

led = 4
#Initialisation de la broche
GPIO.setup(led,GPIO.OUT)

while True:
    #Allumer la LED
    print("LED allumée")
    GPIO.output(led,1)

    #Attendre 5s
    time.sleep(1)

    #Eteindre la LED
    print("LED éteinte")
    GPIO.output(led,0)
    
    time.sleep(1)
