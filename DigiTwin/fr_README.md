# DigiTwin - Génération de Trajectoire Circulaire avec un Manipulateur Robot (Staubli RX160)
### *Pour un aperçu plus complet de mon travail, visitez mon portfolio sur [imonge.es](https://imonge.es/proyecto/2?lang=fr).*
## Description  
Ce projet est un modèle complet de robot RRR, incluant les paramètres de modélisation, les simulations et les tests associés. Il permet les calculs de modélisation géométrique et cinématique ainsi que les simulations de trajectoires.

## Structure des Fichiers
### `const_v.py`
- Contient les constantes définissant le robot RRR.
- Paramètres de distance des axes et paramètres de Denavit-Hartenberg (DH).
### `matrices_tn.py`
- **`matrice_Tim1_Ti(qi, ai_m1, alphai_m1, ri, Debug=False)`**  
  Calcule la matrice de transformation DH entre deux articulations successives.
- **`generate_transformation_matrices(q, dh, round_p=False, Debug=False)`**  
  Génère une liste de matrices de transformation \( T(i, i+1) \) basée sur les paramètres DH.
- **`matrice_Tn(dh, q, Debug=False)`**  
  Calcule la matrice globale \( T0,n \) en utilisant les paramètres DH et les angles articulaires \( q \).
- **`mgd(q, Liaisons, Debug=False)`**  
  Résout la modélisation géométrique directe.
- **`mgi(Xd, Liaisons, Debug=False)`**  
  Résout la modélisation géométrique inverse.
- **`xy_Ot(result_matrix)`**  
  Extrait les coordonnées opérationnelles obtenues de la matrice \( T0,n \).
---
### `modele_differentiel.py`
- Contient les fonctions liées au modèle différentiel du robot, incluant :
  - Jacobiens calculés géométriquement.
  - Jacobiens calculés analytiquement.
  - Modèle Différentiel Direct (MDD).
  - Modèle Différentiel Inverse (MDI).
---
### `trajectory_generation.py`
- **`traj(A, B, V1, V2, K, Debug=False)`**  
  Génère une trajectoire circulaire dans l'espace \( \mathbb{R}^3 \) entre deux points \( A \) et \( B \).  
  **Arguments :**
  - `A`, `B` : Points de départ et d'arrivée \([x, y, z]\).
  - `V1`, `V2` : Vitesses initiale et finale (mm/s).
  - `K` : Accélération.
  - `Debug` : Affiche les détails pour le débogage.  
  **Retourne :**
  - Trajectoires articulaires, vitesses et positions opérationnelles.
---
### `main.py`
- Fichier exécutable principal.
- Permet aux utilisateurs de tester et utiliser toutes les fonctionnalités à travers des interactions guidées.
---
### Tests et Simulations
- Les fichiers auxiliaires contiennent les simulations et tests nécessaires pour valider le modèle et les fonctions.
---
## Utilisation
### 1. Cloner le dépôt
```bash
git clone https://github.com/IsmaTIBU/DigiTwin.git
```
### 2. Installer les dépendances
```bash
pip install -r required.txt
```
### 3. Exécuter le fichier principal
```bash
python src/main.py
```
### 4. Entrées Attendues
  Unités :  
    - Vitesses linéaires : mm/s  
    - Vitesses angulaires : rad/s  
    - Vitesses articulaires : rad/s  
    - Distances : mm
