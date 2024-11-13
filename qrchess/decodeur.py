# Eyub Celebioglu (21902333)
# Vincent Ly      (21904464)

# py –m pip install numpy ou bien pip install numpy
#pip install pillow ou bien py -m pip install pillow

from PIL import Image
import numpy as np

# charger les images des pièces
pieces = {
    "pion_blanc": "images/pion_blanc.png",
    "tour_blanc": "images/tour_blanc.png",
    "cavalier_blanc": "images/cavalier_blanc.png",
    "fou_blanc": "images/fou_blanc.png",
    "reine_blanc": "images/reine_blanc.png",
    "roi_blanc": "images/roi_blanc.png",
    "pion_noir": "images/pion_noir.png",
    "tour_noir": "images/tour_noir.png",
    "cavalier_noir": "images/cavalier_noir.png",
    "fou_noir": "images/fou_noir.png",
    "reine_noir": "images/reine_noir.png",
    "roi_noir": "images/roi_noir.png",
    "reine_noir_retournee": "images/reine_noir_retournee.png",
    "roi_noir_retournee": "images/roi_noir_retournee.png",
    "reine_blanc_retournee": "images/reine_blanc_retournee.png",
    "roi_blanc_retournee": "images/roi_blanc_retournee.png",
    "case_blanche": "images/caseblanche.png",
    "case_grise": "images/casegrise.png",
    "case_noir": "images/casenoir.png"
}


def comparerImages(image1, image2):
    # Redimensionner les images pour qu'elles aient la même taille
    image1_resized = image1.resize(image2.size)
    
    # Convertir les images en niveaux de gris
    image1_gray = image1_resized.convert("L")
    image2_gray = image2.convert("L")
    
    # Convertir les images en tableaux numpy normalisés
    np_image1 = np.array(image1_gray, dtype=np.float32) / 255.0
    np_image2 = np.array(image2_gray, dtype=np.float32) / 255.0
    
    # Aplatir les tableaux en vecteurs
    vec_image1 = np_image1.flatten()
    vec_image2 = np_image2.flatten()
    
    # Calculer le produit scalaire des deux vecteurs
    dot_product = np.dot(vec_image1, vec_image2)
    
    # Calculer les normes des vecteurs
    norm_image1 = np.linalg.norm(vec_image1)
    norm_image2 = np.linalg.norm(vec_image2)
    
    # Calculer la similarité cosinus
    similarity = dot_product / (norm_image1 * norm_image2)
    
    return similarity

def calculMatrice(taille_case,sous_image,diviseur):
    # on utilise le diviseur qui va nous permetre d avoir les dimension de la matrice 
    matrice = [[0] * diviseur for _ in range(diviseur)]

    # comparaison de chaque case avec toutes les images de pièces dechec
    for i in range(diviseur):  # parcours des lignes
        for j in range(diviseur):  # parcours des colonnes
            # coordonnées de la case actuelle
            x1 = j * taille_case/2
            y1 = i * taille_case/2
            x2 = x1 + taille_case/2
            y2 = y1 + taille_case/2
            
            # découper la région correspondante de l'image
            case = sous_image.crop((x1, y1, x2, y2))
            cmp = 0 #permet de comparer pour la corelation
            
            for nom_piece, chemin_image_piece in pieces.items():
                # charger l'image de la pièce
                image_piece = Image.open(chemin_image_piece)
                
                # comparer les images
                similarite = comparerImages(case, image_piece)
                if cmp < similarite :
                    cmp = similarite
                    nom = nom_piece
            matrice[i][j] = nom
            #print(f"Similarité entre la case {i+1},{j+1} et la pièce {nom}: {cmp}")

    # afficher la matrice dans la console
    #for ligne in matrice:
        #print(" ".join(str(element) for element in ligne))

    return matrice

def decryptage(matrice,findeboucle,parite):
    # le msg decrypte
    message = ""

    # map des pieces en fonction de leur chiffrement
    PIECES = {
    "pion_blanc" : 0,
    "tour_blanc" : 1,
    "cavalier_blanc" : 2,
    "fou_blanc" : 3,
    "reine_blanc" : 4,
    "roi_blanc" : 5,
    "pion_noir" : 6,
    "tour_noir" : 7,
    "cavalier_noir" : 8,
    "fou_noir" : 9,
    "reine_noir" : 10,
    "roi_noir" : 11,
    "reine_noir_retournee" : 12,
    "roi_noir_retournee" : 13,
    "reine_blanc_retournee" : 14,
    "roi_blanc_retournee" : 15,
    "case_grise" : 16,
    "case_blanche" : 16,
    "case_noir" : 16
    }

    # remplissage de la matrice
    j = 0
    while j < 7*findeboucle + parite:
        i = 7*findeboucle + parite 
        #print("i :", i, "j :", j,"case ",matrice[i][j])
        #print("je suis la")
        while i > 0:
            if i - 2 > 0 and (matrice[i - 1][j] == "case_grise" and "case_blanche"):
                break  
            elif matrice[i][j] == "case_grise" or matrice[i][j] == "case_noir":
                break
            elif matrice[i][j] == "case_blanche":
                i -= 1  # Décrémentation de i pour les colonne impair
            
            piece2 = matrice[i][j]
            piece1 = matrice[i - 1][j]
            #print(piece1, piece2, "i =", i, "j =", j)
            ascii_nombre1 = (PIECES[piece1])
            ascii_nombre2 = (PIECES[piece2])
            # le premier nombre de 4 bits vers la gauche
            # l'opérateur OU bit à bit pour combiner les deux nombres
            valeur_combinee = (ascii_nombre1 << 4) | ascii_nombre2
            
            #print(str(valeur_combinee))
            caractere_ascii = chr(valeur_combinee)
            message += caractere_ascii
            #print(message)

            i -= 2  # décrémentation de i

        j += 1  # incrémentation de j

    return message

# main
def main():
    # converti les images en objets Image de Pillow
    pieces_pil = {}
    for nom_piece, chemin_image in pieces.items():
        image_pil = Image.open(chemin_image)
        pieces_pil[nom_piece] = image_pil

    # charger l'image du qrchess
    echiquier_image = Image.open("qrchessimage.png")

    x1, y1 = 0, 0  # coin supérieur gauche (coord. x, coord. y)
    x2, y2 = echiquier_image.size # coin inférieur droit
    #print(x2)

    sous_image = echiquier_image.crop((x1, y1, x2/2, y2/2))
    largeur, hauteur = sous_image.size
    #print(largeur)
    #sous_image.show()


    # on definit le qui nous permet de savoir combien de case il ya de carre par rapport a la dimension de limage et donc davoir la dimmesion de la matrice
    diviseur = int(8*largeur/600)
    rapportpourboucle = int(diviseur/8)
    #print(rapportpourboucle)
    parite = rapportpourboucle - 1
    #print(parite)
    #print(diviseur)
    taille_case = x2 // diviseur

    premier_carre = decryptage(calculMatrice(taille_case,sous_image,diviseur),rapportpourboucle,parite)

    # redondance / pour chaque carre qui reste on prend la photo on la pivote puis par rapport au degres de tournage
    x1, y1 = 0, int(y2/2)  # nouveau point pour le carre en (0,1)
    x2, y2 = int(x2/2), y2 
    #print(x1,y1,x2,y2)
    sous_image = echiquier_image.crop((x1, y1, x2, y2))
    largeur, hauteur = sous_image.size
    image_pivotee = sous_image.rotate(-90) #pivote la photo de 90 degre pour la remettre a lendroit et co;parer les peices
    #image_pivotee.show()
    
    deuxieme_carre = decryptage(calculMatrice(taille_case,image_pivotee,diviseur),rapportpourboucle,parite)
    
    # nouveau point pour le carre en (1,1)
    x1, y1 = echiquier_image.size 
    x2, y2 = echiquier_image.size
    #print(x1,y1,x2,y2)
    sous_image = echiquier_image.crop((x1/2, y1/2, x2, y2))
    largeur, hauteur = sous_image.size
    image_pivotee = sous_image.rotate(-180) #pivote la photo de 90 degre pour la remettre a lendroit et co;parer les peices
    #image_pivotee.show()
    
    troisieme_carre = decryptage(calculMatrice(taille_case,image_pivotee,diviseur),rapportpourboucle,parite)

    # nouveau point pour le carre en (1,0)
    x1, y1 = echiquier_image.size 
    x2, y2 = echiquier_image.size
    #print(x1,y1,x2,y2)
    sous_image = echiquier_image.crop((x1/2, 0, x2, y2/2))
    largeur, hauteur = sous_image.size
    image_pivotee = sous_image.rotate(-270) #pivote la photo de 90 degre pour la remettre a lendroit et co;parer les peices
    #image_pivotee.show()
    
    quatrieme_carre = decryptage(calculMatrice(taille_case,image_pivotee,diviseur),rapportpourboucle,parite)
    
    liste_msg = []
    liste_msg.append(premier_carre)
    liste_msg.append(deuxieme_carre)
    liste_msg.append(troisieme_carre)
    liste_msg.append(quatrieme_carre)

    # verifie si toutes les msg sont les memes
    if all(mot == liste_msg[0] for mot in liste_msg):
        mot_resultat = liste_msg[0]
    # verifie si au moins deux msg se ressemblent
    elif len(set(liste_msg)) != len(liste_msg):
        for mot in enumerate(liste_msg):
            if liste_msg.count(mot) > 1:
                mot_resultat = mot
                break
    # si aucun msg ne se ressemble, afficher le plus long
    else:
        mot_resultat = max(liste_msg, key=len)

    # affiche le msg résultat
    print("Le message est :", mot_resultat)
    
if __name__ == "__main__":
    main()




