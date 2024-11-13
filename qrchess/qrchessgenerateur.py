# Eyub Celebioglu (21902333)
# Vincent Ly      (21904464)

# py –m pip install pygame ou bien pip install pygame
#pip install os-sys ou bien py -m pip install os-sys

import pygame as pg
import sys

IMAGES = {}

PIECES = {
    0: "pion_blanc",
    1: "tour_blanc",
    2: "cavalier_blanc",
    3: "fou_blanc",
    4: "reine_blanc",
    5: "roi_blanc",
    6: "pion_noir",
    7: "tour_noir",
    8: "cavalier_noir",
    9: "fou_noir",
    10: "reine_noir",
    11: "roi_noir",
    12: "reine_noir_retournee",
    13: "roi_noir_retournee",
    14: "reine_blanc_retournee",
    15: "roi_blanc_retournee"
}

# on init les peices en recuperent les images et en les transormant en objet pygame pour creer limage ensuite
def initialiserPieces(TAILLE):
    for nom in PIECES.values():
        image = pg.image.load(f"images/{nom}.png")
        IMAGES[nom] = pg.transform.scale(image, (TAILLE, TAILLE))

#on associe une valeur ascii a la piece   
def associerPiece(valeur_ascii):
    nom_piece = PIECES.get(valeur_ascii)
    if nom_piece:
        return IMAGES[nom_piece]
    return None

# on definit la taille de la matrice/plateau en fonction du msg
def definirTaille(msg,dimensionInitial):
    if (len(msg) <= (((dimensionInitial*dimensionInitial)/2)-(dimensionInitial/2))):
        return dimensionInitial
    else :
        return definirTaille(msg, dimensionInitial*2)

# transformation/encodage d'un caractere en ASCII
def encoderCaractere(caractere):
    ascii_value = ord(caractere)  # obtenir la valeur ASCII du caractère
    # divisez les 8 bits de l'ASCII en deux groupes de 4 bits
    groupe1 = ascii_value >> 4  # 4 premiers bits
    groupe2 = ascii_value & 0xF  # 4 derniers bits
    return associerPiece(groupe1), associerPiece(groupe2)  # retourne les pièces correspondantes

# on dessine le plateau d'echec
def dessinerPlateau(ecran,DIMENSION,TAILLE):
    couleurs = [pg.Color("white"), pg.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            couleur = couleurs[(row + col) % 2]
            if (row == 0 and col == DIMENSION - 1) :
                 pg.draw.rect(ecran, pg.Color("black"), pg.Rect(col*TAILLE, row*TAILLE, TAILLE, TAILLE))
            else :
                pg.draw.rect(ecran, couleur, pg.Rect(col*TAILLE, row*TAILLE, TAILLE, TAILLE))

# on place les piece sur le plateau
def placerPieces(ecran, pieces, DIMENSION, TAILLE):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = pieces[row][col]
            if piece is not None:
                ecran.blit(piece, pg.Rect(col*TAILLE, row*TAILLE, TAILLE, TAILLE))

# algo qui permet de placer correctement les pieces par rapport a notre architecture definit dans le pdf
def decoderEtPlacer(chaine,DIMENSION):
    plateau = [[None] * DIMENSION for _ in range(DIMENSION)]
    row, col = DIMENSION - 1, 0  # commencer en bas à gauche (a1 dans un plateau d'echec)
    for caractere in chaine:
        if col%2 == 0 :
            if row < 0 or col >= DIMENSION:  # arrete si nous atteignons la limite supérieure du plateau
                break
            piece2, piece1 = encoderCaractere(caractere)
            # place les pièces en alternant entre les cases noires et blanches
            plateau[row][col] = piece1
            plateau[row-1][col] = piece2
            # passe à la prochaine ligne
            row -= 2
            # si nous atteignons la fin de la collone, passer à la colone précédente
            if row < 0:
                row = DIMENSION - 1
                col += 1
        else :
            #on saute une ligne pour etre dans le noir pour les 4 dernier bits
            if row == DIMENSION - 1 :
                row -= 1
            else :
                row -= 2
            if (row) < 0 or col >= DIMENSION:  # arrete si nous atteignons la limite supérieure du plateau
                break
            piece2, piece1 = encoderCaractere(caractere)
            # place les pièces en alternant entre les cases noires et blanches
            plateau[row][col] = piece1
            plateau[row-1][col] = piece2
    
            # si nous atteignons la fin de la collone, passer à la colone précédente
            if row-4 < 0:
                row = DIMENSION - 1
                col += 1
    return plateau

# permet de tourner une image pour la redondance
def rotationImage(image, angle):
    # rotation de l'image autour de son centre
    rotated_image = pg.transform.rotate(image, angle)
    # recupere le carre entourant l'image
    rotated_ca = rotated_image.get_rect(center=image.get_rect(topleft=(0, 0)).center)
    return rotated_image, rotated_ca

# permet de generer une image
def genererImage(chaine_entree):
    # definir les dimension
    dimension_initiale = 8
    dimension_plateau = definirTaille(chaine_entree, dimension_initiale)
    rapport_fenetre = dimension_plateau / dimension_initiale

    #taille de l'image pour un plateau 8x8 de base puis augmente en fonction de la taille du plateau (x2)
    largeur_capture = longueur_capture = 600
    num = largeur_capture * rapport_fenetre
    largeur_capture = longueur_capture = num

    taille_case = largeur_capture // dimension_plateau

    # initialiser les peices et decoder
    initialiserPieces(taille_case)
    plateau = decoderEtPlacer(chaine_entree, dimension_plateau)


    # initialisation de Pygame
    pg.init()

    # creationn de la surface pour l'image
    image_surface = pg.Surface((largeur_capture*2, longueur_capture*2))
    image_surface.fill(pg.Color("white"))

    # dessine le QRChess d'origine à la position (0, 0) (voir ca comme une matrice de 2x2)
    ecran_0_0 = pg.Surface((largeur_capture, longueur_capture))
    ecran_0_0.fill(pg.Color("white"))
    dessinerPlateau(ecran_0_0, dimension_plateau, taille_case)
    placerPieces(ecran_0_0, plateau, dimension_plateau, taille_case)
    image_surface.blit(ecran_0_0, (0, 0))

    # dessine une copie du QRChess à la position (1, 0) avec une rotation de 90 degrés
    ecran_1_0 = pg.Surface((largeur_capture, longueur_capture))
    ecran_1_0.fill(pg.Color("white"))
    dessinerPlateau(ecran_1_0, dimension_plateau, taille_case)
    placerPieces(ecran_1_0, plateau, dimension_plateau, taille_case)
    ecran_1_0_rotated = pg.transform.rotate(ecran_1_0, -90)
    image_surface.blit(ecran_1_0_rotated, (largeur_capture, 0))

    # dessine une copie du QRChess à la position (1, 1) avec une rotation de 180 degrés
    ecran_1_1 = pg.Surface((largeur_capture, longueur_capture))
    ecran_1_1.fill(pg.Color("white"))
    dessinerPlateau(ecran_1_1, dimension_plateau, taille_case)
    placerPieces(ecran_1_1, plateau, dimension_plateau, taille_case)
    ecran_1_1_rotated = pg.transform.rotate(ecran_1_1, -180)
    image_surface.blit(ecran_1_1_rotated, (largeur_capture, longueur_capture))

    # dessine une copie du QRChess à la position (0, 1) avec une rotation de 270 degrés
    ecran_0_1 = pg.Surface((largeur_capture, longueur_capture))
    ecran_0_1.fill(pg.Color("white"))
    dessinerPlateau(ecran_0_1, dimension_plateau, taille_case)
    placerPieces(ecran_0_1, plateau, dimension_plateau, taille_case)
    ecran_0_1_rotated = pg.transform.rotate(ecran_0_1, -270)
    image_surface.blit(ecran_0_1_rotated, (0, longueur_capture))

    # enregistre l'image dans le fichier qrchess
    nom_fichier_image = "qrchessimage.png"
    pg.image.save(image_surface, nom_fichier_image)

    # quite pygame
    pg.quit()

# permet dafficher ce qu'on a cree
def afficherImage(image):

    # initialisation de Pygame
    pg.init()

    # chargement de l'image
    image = pg.image.load(image)

    # dimensions de la fenêtre d'affichage pour l'utilsateur pour qu'il visualise en avant premiere a quoi ca ressemble
    largeur_fenetre = 500
    hauteur_fenetre = 500
    dimensions_fenetre = (largeur_fenetre, hauteur_fenetre)

    # creation de la fenêtre
    fenetre = pg.display.set_mode(dimensions_fenetre)
    pg.display.set_caption("Affichage de l'image")

    # redimensionne l'image à la taille de la fenêtre
    image_redimensionnee = pg.transform.scale(image, dimensions_fenetre)

    # affichage de l'image
    fenetre.blit(image_redimensionnee, (0, 0))
    pg.display.flip()

    # montre pendant 10 secondes
    pg.time.wait(10000)

    # puis quitte pygame et le programme
    pg.quit()
    sys.exit()

# main pour lancer les algo
def main():
    chaine_entree = input("Entrez la chaîne de caractères : ")
    genererImage(chaine_entree)
    image = "qrchessimage.png"
    afficherImage(image)      
    

if __name__ == "__main__":
    main()

