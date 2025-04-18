#!/usr/bin/python3
import hashlib,argparse,sys,math,os

# Affichier l'utilisation du script
desc = "Calcul hash de fichier\npar : Sivanesan"
# Création de parser avec la variable utilisation
parser=argparse.ArgumentParser(description=desc)
parser.add_argument("-f", "--fichier", dest="fichier",help="Fichier à hasher", required=True)
parser.add_argument("-v", "--verifier", dest="hash",help="Fichier avec Hash a vérifier")
parser.add_argument("-m", "--methode", dest="methode",help="Méthode de hash souhaité", default="sha256")

args=parser.parse_args()

# Calcul du hash256
BLOCK = 65536

if args.methode == "sha256" :
    hasher = hashlib.sha256()
else:
    if args.methode == "sha512" :
        hasher = hashlib.sha512()
    else:
        print("\nAttention méthode de hash incorrecte!")
        sys.exit(1)

# Obtenir la taille totale du fichier en octets
total_size = os.path.getsize(args.fichier)

# Initialiser les variables pour suivre la progression
hashed_size = 0

with open(args.fichier, 'rb') as fichier:
    buf = fichier.read(BLOCK)
    while len(buf) > 0:
        hasher.update(buf)
        hashed_size += len(buf)
        percent_hashed = hashed_size / total_size
        progress = math.floor(percent_hashed * 50)
        print(f"\rCalcul du hash: [{'#' * progress}{'-' * (50 - progress)}] {format(percent_hashed * 100, '.1f')}%", end="")
        buf = fichier.read(BLOCK)

sha=hasher.hexdigest()
print(f"\nLe hash du fichier {args.fichier} est : {sha}")

if args.hash:
    with open(args.hash, 'r') as h:
        verif=h.read().split()
        for ligne in verif:
            if sha.upper() in ligne.split('"'):
                print("\nLes deux hash sont identiques")
                sys.exit(0)
            elif sha.lower() in ligne.split('"'):
                print("\nLes deux hash sont identiques")
                sys.exit(0)
    print("\nLes deux hash ne sont pas identiques !")

