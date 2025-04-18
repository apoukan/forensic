#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse,sys,os.path,subprocess,struct

#Partie MBR
class EnregistrementMbr():
    def __init__(self, sector):
        fmt=('<446s' + # Boot code
                # partition 1
		'B' + # Active flag 0x80 is active (bootable)
		'B' + # Start head
		'B' + # Start sector only bits 0-5 bits 6-7 for cylinder
		'B' + # Start cylinder (upper 2 bits in previous byte)
		'B' + # partition type code (7 si NTFS)
		'B' + # End head
		'B' + # End sector
		'B' + # End cylinder
		'I' + # Sectors preceeding partition
		'I' + # Sectors in partition
		# partition 2
		'B'+'B'+'B'+'B'+'B'+'B'+'B'+'B'+'I'+'I'+ \
		# partition 3
		'B'+'B'+'B'+'B'+'B'+'B'+'B'+'B'+'I'+'I'+ \
		# partition 4
		'B'+'B'+'B'+'B'+'B'+'B'+'B'+'B'+'I'+'I'+ \
		'2s') # Signature de mbr 0x55 0xAA
        self.MBR = struct.unpack(fmt, sector)
        
    def isActive(self, partno):
        #on vérifie si la partition est active avec le code \x80
        if self.MBR[1+10*(partno-1)]==0x80 :
            return "Vrai"
        else :
            return "Faux"
    def partitionType(self, partno):
        return self.MBR[5+10*(partno-1)]
    def isEmpty(self, partno):
        return self.partitionType(partno)==0
    def reservedSectors(self, partno):
        return self.MBR[9+10*(partno-1)]
    def totalSectors(self, partno):
        return self.MBR[10+10*(partno-1)]
    def validSignature(self):
        # Vérification de la signature a la fin du secteur (\x55\xAA)
        return self.MBR[41]==b'\x55\xAA'

    def partition(self):
        print('\n#### Disque MBR ####')
        for i in range(1, 5):
            print(f'Partition {i}:')
            if self.isEmpty(i):
                print("\tL'entrée est vide.")
            else:
                print('\tBootable:', self.isActive(i))
                print('\tType de partition:', self.partitionType(i))
                print('\tDébut secteur:', self.reservedSectors(i))
                secteurs=self.totalSectors(i)
                print('\tTotal secteur:', secteurs)
                print("\tTaille:", tailleHumain(secteurs),'\n')
#Partie GPT
supportedParts = ["EBD0A0A2-B9E5-4433-87C0-68B6B72699C7", # Windows Basic data
        "37AFFC90-EF7D-4E96-91C3-2D7AE055B174", # Windows
        "0FC63DAF-8483-4772-8E79-3D69D8477DE4", # Linux filesystem
        "8DA63339-0007-60C0-C436-083AC8230908", # Linux Reserved
        "933AC7E1-2EB4-4F13-B844-0E14E2AEF915", # Linux /home
        "44479540-F297-41B2-9AF7-D131D5F0458A",
        "4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709",
        "B921B045-1DF0-41C3-AF44-4C6F280D3FAE",
        "3B8F8425-20E0-4F3B-907F-1A25A76F98E8",
        "E6D6D379-F507-44C2-A23C-238F2A3DF928",
        "516E7CB4-6ECF-11D6-8FF8-00022D09712B",
        "83BD6B9D-7F41-11DC-BE0B-001560B84F0F",
        "516E7CB5-6ECF-11D6-8FF8-00022D09712B",
        "85D5E45A-237C-11E1-B4B3-E89A8F7FC3A7",
        "516E7CB4-6ECF-11D6-8FF8-00022D09712B",
        "824CC7A0-36A8-11E3-890A-952519AD3F61",
        "55465300-0000-11AA-AA11-00306543ECAC",
        "516E7CB4-6ECF-11D6-8FF8-00022D09712B",
        "49F48D5A-B10E-11DC-B99B-0019D1879648",
        "49F48D82-B10E-11DC-B99B-0019D1879648",
        "2DB519C4-B10F-11DC-B99B-0019D1879648",
        "2DB519EC-B10F-11DC-B99B-0019D1879648",
        "49F48DAA-B10E-11DC-B99B-0019D1879648",
        "426F6F74-0000-11AA-AA11-00306543ECAC",
        "48465300-0000-11AA-AA11-00306543ECAC",
        "52414944-0000-11AA-AA11-00306543ECAC",
        "52414944-5F4F-11AA-AA11-00306543ECAC",
        "4C616265-6C00-11AA-AA11-00306543ECAC",
        "6A82CB45-1DD2-11B2-99A6-080020736631",
        "6A85CF4D-1DD2-11B2-99A6-080020736631",
        "6A898CC3-1DD2-11B2-99A6-080020736631",
        "6A8B642B-1DD2-11B2-99A6-080020736631",
        "6A8EF2E9-1DD2-11B2-99A6-080020736631",
        "6A90BA39-1DD2-11B2-99A6-080020736631",
        "6A9283A5-1DD2-11B2-99A6-080020736631",
        "75894C1E-3AEB-11D3-B7C1-7B03A0000000",
        "E2A1E728-32E3-11D6-A682-7B03A0000000",
        "BC13C2FF-59E6-4262-A352-B275FD6F7172",
        "42465331-3BA3-10F1-802A-4861696B7521",
        "AA31E02A-400F-11DB-9590-000C2911D1B8",
        "9198EFFC-31C0-11DB-8F78-000C2911D1B8",
        "9D275380-40AD-11DB-BF97-000C2911D1B8",
        "A19D880F-05FC-4D3B-A006-743F0F84911E"]
def printGuid(packedString):
    if len(packedString) == 16:
        outstr = format(struct.unpack('<L', packedString[0:4])[0], 'X').zfill(8) + "-" + \
                format(struct.unpack('<H', packedString[4:6])[0], 'X').zfill(4) + "-" + \
                format(struct.unpack('<H', packedString[6:8])[0], 'X').zfill(4) + "-" + \
                format(struct.unpack('>H', packedString[8:10])[0], 'X').zfill(4) + "-" + \
                format(struct.unpack('>Q', b"\x00\x00" + packedString[10:16])[0], 'X').zfill(12)
    else:
        outstr = "<invalid>"
    return outstr

class GptRecord():
    def __init__(self, recs, partno):
        self.partno = partno
        offset = partno * 128
        self.empty = False
        # Créer un type de partition GUID en str
        self.partType = printGuid(recs[offset:offset+16])
        if self.partType == "00000000-0000-0000-0000-000000000000":
            self.empty = True
        self.partGUID = printGuid(recs[offset+16:offset+32])

        self.firstLBA = struct.unpack('<Q', recs[offset+32:offset+40])[0]
        self.lastLBA = struct.unpack('<Q', recs[offset+40:offset+48])[0]
        self.attr = struct.unpack('<Q', recs[offset+48:offset+56])[0]
        nameIndex = recs[offset+56:offset+128].find(b'\x00\x00')
        if nameIndex != -1:
            self.partName = recs[offset+56:offset+56+nameIndex].decode("utf-8", "replace")
        else:
            self.partName = recs[offset+56:offset+128].decode("utf-8", "replace")
            
    def printPart(self):
        if not self.empty:
            outstr = str(self.partno+1) + ":" + str(self.partType) + ":" + str(self.partGUID) + \
                    ":" + str(self.firstLBA) + ":" + str(self.lastLBA) + ":" + \
                    str(self.attr) + ":" + self.partName
            print(outstr)

#Conversion de taille depuis secteur
def tailleHumain(secteur):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    size=secteur*512
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return f"{size:.2f} {suffixes[suffixIndex]}"

#peripherique de bouclage pour pouvoir monter 2 partitions a partir d'un meme fichier
def perif_boucle(args,action=True):
    try :
    	#on efface les loop deja crée non utilisé
    	effacement=subprocess.check_output(["losetup","-D"],stderr=subprocess.STDOUT)
    	if action:
    		try:
    			#on cree des interfaces loop par partition
    			loop=subprocess.check_output(["losetup","-f","-P","-r","--show",args.disque],stderr=subprocess.STDOUT)
    			return loop.decode().rstrip()
    		except Exception as ex: 
    			print("Erreur lors de la création du périphérique de bouclage.\n",ex)
    			sys.exit(1)
    except :
        pass

#montage de partitions
def montage(numero,loop,args):
	try:
	    mountpath = args.localisation + numero
	    #cree le rep s'il n'existe pais
	    if not os.path.isdir(mountpath):
	       	subprocess.call(['mkdir', mountpath])
	    
	    mountopts = (args.options)
	    mountloop=loop+"p"+numero
	    out=subprocess.check_output(['mount', '-o', mountopts,mountloop,mountpath],stderr=subprocess.STDOUT)
	    print(f"[+]La partition {numero} est monté! dans [{mountpath}]")
	except Exception as ex:
	    effacement=subprocess.check_output(["losetup","-D"],stderr=subprocess.STDOUT)
	    print("Une erreur s'est produite pendant le montage:\n",ex)

#Demonter les partitions par rapport au fichier sources
def demontage(numero,args):
	try:
		mountpath = args.localisation + numero
		out=subprocess.check_output(['umount',mountpath],stderr=subprocess.STDOUT)
		print(f"[-]La partition {numero} est démonté!")
		effacement=subprocess.check_output(["losetup","-D"],stderr=subprocess.STDOUT)
	except Exception as ex:
		effacement=subprocess.check_output(["losetup","-D"],stderr=subprocess.STDOUT)
		print("Une erreur s'est produite pendant le démontage:\n",ex)

#traiter le MBR
def partie_mbr(mbr,args):
	#partitions non supportes par le script en MBR
	PartsNoSupp = [0x05, 0x0f, 0x85, 0x91, 0x9b, 0xc5, 0xe4, 0xee]
	swapParts = [0x42, 0x82, 0xb8, 0xc3, 0xfc]
	loop=perif_boucle(args)
	
	#Affiche les partitions si vous avez choisie l'option "-v"
	if args.verifie:
		mbr.partition()
	for i in range(1,5):
		if not mbr.isEmpty(i):
			if mbr.partitionType(i) in PartsNoSupp:
				print("Désolé, les partitions étendues ne sont pas pris en charge par ce script!")
			else:
				if mbr.partitionType(i) in swapParts:
					print("Partition swap ignorée")
				else:
					if args.monter:
						montage(str(i),loop,args)
					elif args.enlever:
						demontage(str(i),args)
						

#traiter le GPT
def partie_gpt(mbr,args):
    # vérifiez l'en-tête comme un autre contrôle de quality
    with open(args.disque, 'rb') as f:
        f.seek(512)
        sector = f.read(512)
        if sector[0:8] != b"EFI PART":
            print("Vous semblez manquer un en-tête GUID")
            sys.exit(1)
        print("L'en-tête de la table de partition MBR et GUID de protection valide trouvé")
        with open(args.disque, 'rb') as f:
            f.seek(1024)
            partRecs = f.read(512 * 32)
            parts = [ ]
            boucle=perif_boucle(args=args)
            for i in range(0, 128):
                p = GptRecord(partRecs, i)
                if not p.empty:
                    if args.verifie:
                        p.printPart()
                        perif_boucle(args,action=False)
                    parts.append(p)
            for p in parts:
                if p.partType in supportedParts:
                    if args.monter:
                        numero=str(p.partno+1)
                        loop=boucle
                        args=args
                        montage(numero,loop,args)
                    elif args.enlever:
                        demontage(args=args,numero=str(p.partno+1))
							
		
#programme principale
def main():
    #Affichier l'utilisation du script
    desc = "Script de Montage de partition depuis MBR ou GPT\npar : Sivanesan"
    #Création de parser avec la variable utilisation
    parser=argparse.ArgumentParser(description=desc)
    parser.add_argument("-d", "--disque", help="Disque du sujet a monté ou analysé", required=True)
    parser.add_argument("-v", "--verifie", help="Permet d'affciher le type de disque et les partitions",action='store_true')
    parser.add_argument("-m", "--monter", help="Permet de monter les partitions par défaut dans '/mnt/'",action='store_true')
    parser.add_argument("-e", "--enlever", help="Permet de démonter les partitions", action='store_true')
    parser.add_argument("-l", "--localisation", help="Permet de préciser où monter les partions", default="/mnt/sujet")
    parser.add_argument("-o", "--options", help="Permet de préciser les options de la commande 'mount'", default="loop,ro,noatime,noload")


    #On récupère les arguments
    args=parser.parse_args()

    #Vérifie s'il y a un argument 
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
		
    if not args.monter and args.enlever:
        args.verifie = True

    # Vérification si le paramètre entrer est un fichier
    if not os.path.isfile(args.disque):
    	print("Fichier " + args.disque + " ne peut pas être ouvert pour la lecture")
    	exit(1)
    if args.enlever:
    	perif_boucle(args,action=False)
		
    # lire le premier secteur et uniquement les 512 octets en binaire 
    with open(args.disque, 'rb') as f:
        sector = f.read(512)
	
    mbr=EnregistrementMbr(sector) # Création de l'objet MBR
	
    #On vérifie que dans les 512 octets il y a bien un MBR
    if mbr.validSignature():
    	if mbr.partitionType(1) == 0xee:
    		partie_gpt(mbr,args)
    	else :
    		partie_mbr(mbr,args)
    
    else:
        print("Ne semble pas contenir un MBR valide")

if __name__ == "__main__":
    main()
