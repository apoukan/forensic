#!/usr/bin/python3

import hashlib,optparse,sys

#Affichier l'utilisation du script
utilisation = "%prog -f <fichier> [-v <fichier hash> -m <sha256 ou sha512>]"
#Création de parser avec la variable utilisation
parser=optparse.OptionParser(usage=utilisation)
parser.add_option("-f", "--fichier", dest="fichier",help="Fichier à hasher")
parser.add_option("-v", "--verifier", dest="hash",help="Fichier avec Hash a vérifier")
parser.add_option("-m", "--methode", dest="methode",help="Méthode de hash souhaité")

(options, args)=parser.parse_args()

# Le fichier est une option obligatoire
if not options.fichier:
	print("\nCe script a besoin d'un fichier à calculer en sha256 ou en sha512\n")
	print("Par exemple :",sys.argv[0],"-f sujet.img -m sha256\n")
	sys.exit(1)

if not options.methode:
	print("\nCe script a besoin d'une méthode de hash a calculer\n")
	print("Par exemple :",sys.argv[0],"-f sujet.img -m sha512\n")
	sys.exit(1)

#calcul du hash256
BLOCK = 65536

if options.methode == "sha256" :
	hasher = hashlib.sha256()
else:
	if options.methode == "sha512" :
		hasher = hashlib.sha512()
	else:
		print("\nAttention méthode de hash incorrecte!")
		sys.exit(1)

with open(options.fichier, 'rb') as fichier:
    buf = fichier.read(BLOCK)
    while len(buf) > 0:
        hasher.update(buf)
        buf = fichier.read(BLOCK)

sha=hasher.hexdigest()
print("Le hash du fichier",options.fichier, "est :",sha)

if options.hash:
	with open(options.hash, 'r') as h:
		verif=h.read().split()
		if sha in verif:
			print("\nLes deux hash sont identiques")

		else:
			print("\nLes deux hash ne sont pas identiques !")


