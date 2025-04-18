# Outils d'Analyse Forensique - Python

Ce dépôt contient une suite d'outils développés en Python pour des besoins d'analyse forensique, destinés à l'extraction, la vérification et l'interprétation de données issues de supports numériques (images disques, fichiers, etc.).

## Objectifs

- **Analyse de partitionnement MBR & GPT**
- **Vérification d'intégrité de fichiers (hash)**
- **Montage de partitions à partir d’images disques**
- **Comparaison de hachages pour détection de falsification**

---

## 1. Script : `safemount.py`

### 🛠 Description
Ce script permet l'analyse structurée d'une image disque en lisant les entêtes MBR ou GPT, tout en extrayant les métadonnées associées aux partitions.

### 📁 Fonctionnalités
✅ Analyse des partitions MBR (jusqu'à 4 entrées).

✅ Vérification de la validité de la signature MBR.

✅ Identification des types de partitions (NTFS, Linux, etc.).

✅ Détection des partitions GPT avec GUID standardisés.

✅ Affichage des informations GPT : type, GUID, nom, plage de secteurs, attributs.

✅ Montage automatique des partitions via losetup et mount.

✅ Démontage propre des partitions.

✅ Conversion de la taille des partitions en format lisible (KB, MB, GB...).

### 📦 Exécution

```bash
sudo python3 safemount.py -d /chemin/image.dd -l /mnt/analyse -m
```
## 2. Script : `hasher.py`

### 🛠 Description
Script permettant de calculer le hash d’un fichier (SHA-256 ou SHA-512), avec affichage de la progression, et de vérifier la correspondance avec un hash fourni dans un fichier texte.

### 📁 Fonctionnalités

✅ Calcul dynamique de hash avec barre de progression

✅ Support des algorithmes SHA-256 (par défaut) et SHA-512

✅ Comparaison automatique avec un fichier contenant un ou plusieurs hash

### 📦 Exécution

```bash
sudo python3 hasher.py -f /chemin/image.jpg
```
