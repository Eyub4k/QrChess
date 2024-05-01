import pygame as pg

LARGEUR = LONGUEUR = 512
DIMENSION = 8
TAILLE = LARGEUR // DIMENSION
IMAGES = {}

PIECES = {
    0: "pion_blanc_retournee",
    1: "pion_blanc",
    2: "tour_blanc",
    3: "cavalier_blanc",
    4: "fou_blanc",
    5: "reine_blanc",
    6: "roi_blanc",
    7: "pion_noir",
    8: "tour_noir",
    9: "cavalier_noir",
    10: "fou_noir",
    11: "reine_noir",
    12: "roi_noir",
    13: "reine_noir_retournee",
    14: "roi_noir_retournee",
    15: "reine_blanc_retournee",
    16: "roi_blanc_retournee"
}

def initialiserPieces():
    for piece, nom in PIECES.items():
        IMAGES[nom] = pg.image.load(f"images/{nom}.png")

def associerPiece(valeur_ascii):
    nom_piece = PIECES.get(valeur_ascii)
    if nom_piece:
        return IMAGES[nom_piece]
    return None


def encoderCaractere(caractere):
    ascii_value = ord(caractere)  # Obtenir la valeur ASCII du caractère
    # Divisez les 8 bits de l'ASCII en deux groupes de 4 bits
    groupe1 = ascii_value >> 4  # Les 4 premiers bits
    groupe2 = ascii_value & 0xF  # Les 4 derniers bits
    return associerPiece(groupe1), associerPiece(groupe2)  # Retourne les pièces correspondantes

def dessinerPlateau(ecran):
    couleurs = [pg.Color("white"), pg.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            couleur = couleurs[(row + col) % 2]
            if (row == 0 and col == DIMENSION - 1) :
                 pg.draw.rect(ecran, pg.Color("black"), pg.Rect(col*TAILLE, row*TAILLE, TAILLE, TAILLE))
            else :
                pg.draw.rect(ecran, couleur, pg.Rect(col*TAILLE, row*TAILLE, TAILLE, TAILLE))
    

def placerPieces(ecran, pieces):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = pieces[row][col]
            if piece is not None:
                ecran.blit(piece, pg.Rect(col*TAILLE, row*TAILLE, TAILLE, TAILLE))


def decoderEtPlacer(chaine):
    plateau = [[None] * DIMENSION for _ in range(DIMENSION)]
    row, col = DIMENSION - 1, 0  # Commencer en bas à gauche (a1)
    for caractere in chaine:
        if col%2 == 0 :
            if row < 0 or col >= DIMENSION:  # Arrêter si nous atteignons la limite supérieure du plateau
                break
            piece2, piece1 = encoderCaractere(caractere)
            # Placer les pièces en alternant entre les cases noires et blanches
            plateau[row][col] = piece1
            plateau[row-1][col] = piece2
            # Passer à la prochaine ligne
            row -= 2
            # Si nous atteignons la fin de la collone, passer à la colone précédente
            if row < 0:
                row = DIMENSION - 1
                col += 1
        else :
            #on saute une ligne pour etre dans le noir pour les 4 dernier bits
            if row == DIMENSION - 1 :
                row -= 1
            else :
                row -= 2
            if (row) < 0 or col >= DIMENSION:  # Arrêter si nous atteignons la limite supérieure du plateau
                break
            piece2, piece1 = encoderCaractere(caractere)
            # Placer les pièces en alternant entre les cases noires et blanches
            plateau[row][col] = piece1
            plateau[row-1][col] = piece2
    
            # Si nous atteignons la fin de la collone, passer à la colone précédente
            if row-4 < 0:
                row = DIMENSION - 1
                col += 1
    return plateau


def main():
    pg.init()
    ecran = pg.display.set_mode((LARGEUR, LONGUEUR))
    pg.display.set_caption("QRChess")
    horloge = pg.time.Clock()

    initialiserPieces()

    chaine_entree = input("Entrez la chaîne de caractères : ")
    plateau = decoderEtPlacer(chaine_entree)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        ecran.fill(pg.Color("white"))  # On efface l'écran
        dessinerPlateau(ecran)  # On dessine le plateau
        placerPieces(ecran, plateau)  # On place les pièces d'échecs

        pg.display.flip()
        horloge.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
