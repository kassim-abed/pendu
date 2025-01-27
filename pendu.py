import pygame 

pygame.init() 

color = (255,255,255) 
rect_color = (255,0,0) 

# CREATING CANVAS 
canvas = pygame.display.set_mode((500,500)) 

# TITLE OF CANVAS 
pygame.display.set_caption("Show Image") 

image = pygame.image.load("Screenshot.png") 
exit = False

while not exit: 
	canvas.fill(color) 
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			exit = True

	pygame.draw.rect(canvas, rect_color, 
					pygame.Rect(30,30,60,60)) 
	pygame.display.update() 


import random

# Liste de mots possibles
mots = ["ordinateur", "python", "programmer", "intelligence", "artificielle"]

# Sélectionne un mot aléatoire de la liste
mot_a_deviner = random.choice(mots).upper()
lettres_trouvees = ["_"] * len(mot_a_deviner)
tentatives_restantes = 6
lettres_utilisees = []

print("Bienvenue au jeu du pendu !")

while tentatives_restantes > 0 and "_" in lettres_trouvees:
    print("\nMot à deviner : ", " ".join(lettres_trouvees))
    print("Tentatives restantes : ", tentatives_restantes)
    print("Lettres utilisées : ", " ".join(lettres_utilisees))
    
    lettre = input("Devinez une lettre : ").upper()
    
    if lettre in lettres_utilisees:
        print("Vous avez déjà utilisé cette lettre.")
    elif lettre in mot_a_deviner:
        for index, char in enumerate(mot_a_deviner):
            if char == lettre:
                lettres_trouvees[index] = lettre
    else:
        tentatives_restantes -= 1
        lettres_utilisees.append(lettre)
        print("Lettre incorrecte.")
    
    lettres_utilisees.append(lettre)

if "_" not in lettres_trouvees:
    print("\nFélicitations ! Vous avez deviné le mot : ", mot_a_deviner)
else:
    print("\nDommage ! Vous avez perdu. Le mot était : ", mot_a_deviner)
