#Ce fichier contient un programme python qui pourait être vue comme un jeu
# L'utilisateur dispose de trois curseurs (en vert à droite de l'écran)  qui lui permettent de modifier l'intensité du rouge, du bleu et du vert dans l'image
# Le premier curseur est pour le rouge, le duxieme pour le vert, et le dernier pour le bleu
# Pour changer de curseur, l'utilisateur appui sur les touches "LEFT" et "RIGHT" du clavier
# Et pour changer l'intensité d'une couleur, il dispose des touches "UP" et "DOWN" du clavier
# Pour changer d'image, l'utilisateur appui sur la touche "ENTER" du clavier

#Les images sont contenues dans un dossier nommé "IMG_FILTRE_SPECIALs"


import numpy
import pygame
import threading
import os

pygame.init()
width=910
heigth=600
pygame.display.set_caption("FILTRE")
screen=pygame.display.set_mode((width, heigth))
run=True                  
os.chdir("IMG_FILTRE_SPECIAL")
liste_images=os.listdir()
os.chdir("..") 
image=pygame.surfarray.array3d(pygame.image.load("IMG_FILTRE_SPECIAL/"+liste_images[0]))


class Filtre:
    def __init__(self):
        self.image_afficher=pygame.image.load("IMG_FILTRE_SPECIAL/"+liste_images[0])
        self.image_afficher=pygame.transform.scale(self.image_afficher, (width-320, heigth)) 
        self.indice_image=0
        self.liste_barres=[[width-300, heigth-255], [width-200, heigth-255], [width-100, heigth-255]]
        self.selectionne=[self.liste_barres[0][0], self.liste_barres[0][1], 0]
        self.modification=False
        self.liste_curseurs=[[self.liste_barres[0][0]-10, heigth-5], [self.liste_barres[1][0]-10, heigth-5], [self.liste_barres[2][0]-10, heigth-5]]


    def filtrage(self):
        global image
        global liste_images
        if self.modification==True:
            image=pygame.surfarray.array3d(pygame.image.load("IMG_FILTRE_SPECIAL/"+liste_images[self.indice_image]))
            """pourcentage_rouge=-(self.liste_curseurs[0][1]-heigth)/255
            pourcentage_bleu=-(self.liste_curseurs[1][1]-heigth)/255
            pourcentage_vert=-(self.liste_curseurs[2][1]-heigth)/255"""    
            image=image-image*numpy.array([-(self.liste_curseurs[0][1]-heigth)/255, -(self.liste_curseurs[1][1]-heigth)/255, -(self.liste_curseurs[2][1]-heigth)/255]) 
            image=image.astype(numpy.uint8)
            self.image_afficher=pygame.surfarray.make_surface(image)
            self.image_afficher=pygame.transform.scale(self.image_afficher, (width-320, heigth))
    
    def afficheur(self):
        screen.blit(self.image_afficher, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (self.selectionne[0]-20, self.selectionne[1]-20, 45, 275), 1)
        for element in self.liste_barres:
            pygame.draw.rect(screen, (10, 200, 100), (element[0], element[1], 5, 255))
        for element in self.liste_curseurs:
            pygame.draw.rect(screen, (200, 13, 20), (element[0], element[1], 25, 5))
        pygame.display.flip()

    def verification_touches(self):
        global run
        self.modification=False
        global image
        global liste_images
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                run=False
                break 
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    if self.selectionne[2]==2:
                        self.selectionne[2]=0
                        self.selectionne=[self.liste_barres[0][0], self.liste_barres[0][1], 0]
                    else:
                        self.selectionne[0]=self.selectionne[0]+100
                        self.selectionne[2]=self.selectionne[2]+1
                    screen.fill(0)
                elif  event.key==pygame.K_LEFT:
                    if self.selectionne[2]==0:
                        print("\a")
                    else:
                        self.selectionne[0]=self.selectionne[0]-100
                        self.selectionne[2]=self.selectionne[2]-1
                    screen.fill(0)
                elif event.key==pygame.K_RETURN:
                    if self.indice_image+1==len(liste_images):
                        self.indice_image=0
                    else:
                        self.indice_image=self.indice_image+1
                    image=pygame.surfarray.array3d(pygame.image.load("IMG_FILTRE_SPECIAL/"+liste_images[self.indice_image]))
                    print(liste_images[self.indice_image])
                    self.image_afficher=pygame.surfarray.make_surface(image)
                    self.image_afficher=pygame.transform.scale(self.image_afficher, (width-320, heigth))

        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP] and (self.liste_curseurs[self.selectionne[2]][1]-1)>=(heigth-255):
            self.liste_curseurs[self.selectionne[2]][1]=self.liste_curseurs[self.selectionne[2]][1]-1
            self.modification=True
            screen.fill(0)
        elif keys[pygame.K_DOWN] and (self.liste_curseurs[self.selectionne[2]][1]+1)<=heigth:
            self.liste_curseurs[self.selectionne[2]][1]=self.liste_curseurs[self.selectionne[2]][1]+1
            self.modification=True
            screen.fill(0)
        

filtre=Filtre()

while run:
    th1=threading.Thread(target=filtre.verification_touches())
    th2=threading.Thread(target=filtre.afficheur())
    th3=threading.Thread(target=filtre.filtrage())

    th1.start()
    th2.start()
    th3.start()

    th1.join()
    th2.join()
    th3.join()

