#!/usr/bin/env python2.7
# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Le GPIO 23 est initialisé en entrée. Il est en pull-up pour éviter les faux signaux
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print "Veuillez vérifier que vous avez un bouton connecté de telle maniere"
print "qu il connecte le port GPIO 23 (pin 16) au GND (pin 6)\n"
raw_input("Pressez Entree quand vous etes pret\n>")

print "En attente de signal sur le port GPIO 23"
# a partir de la, le script ne fera plus rien jusqu a ce que 
# le signal sur le port 23 commence à chuter vers zéro. C'est
# la raison pour laquelle nous avons utilisé le pull-up pour 
# garder le signal "HIGH" et empecher un faux signal

print "Pendant ce temps votre Rapsberry Pi ne gaspille pas" 
print "de ressources en attendant un appui sur le bouton.\n"
print "Pressez le bouton quand vous voulez lancer un signal."
try:
    GPIO.wait_for_edge(23, GPIO.FALLING)
    print "\nAppui detecte. Maintenant votre script va"
    print "effectuer l'action correspondant a un appui sur le bouton."
except KeyboardInterrupt:
    GPIO.cleanup()       # reinitialisation GPIO lors d'une sortie CTRL+C
GPIO.cleanup()           # reinitialisation GPIO lors d'une sortie normale
