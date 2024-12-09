<h1 align="center">
  
  Projet de NSI N°2 : FNAP
  
![image](https://github.com/user-attachments/assets/165ae079-4226-4c7f-84eb-88d104f6c3f2)
![image](https://github.com/user-attachments/assets/c8e71f08-2f96-47b9-8bd3-5e5738a868b1)

  <img src="http://ForTheBadge.com/images/badges/built-with-swag.svg">
  <img src="https://forthebadge.com/images/badges/made-with-python.svg">
</h1>

# 👨‍💼 • Membres :
### Classe de 1ere 4, Cours de Mr Pioche
* #### Célestin → [GoldyRat](https://github.com/GoldyRat)
* #### Mateo → [El1teW0lf](https://github.com/El1teW0lf)
* #### Victor → [Herasium](https://github.com/Herasium)
* #### Benjamin → [Ben-cpu-gpu](https://github.com/Ben-cpu-gpu)

# ⚙️ • Fonctionnement :

### [Clique sur le lien 👈]((https://github.com/El1teW0lf/2024_2025__p04_projet2_n1/blob/main/fonctionnement.md))

### **Structure du Script**

#### **Imports**
Le script importe plusieurs modules essentiels :
- `scenes`: Définit probablement des scènes comme `TestWorld` et `MainMenu`.
- `ShowBase` (de `direct.showbase.ShowBase`): Classe de base pour les applications Panda3D.
- `parse_json` (de `modules`): Pas utilisé dans le script visible.
- `BulletWorld` (de `panda3d.bullet`): Gère la physique avec Bullet.
- `Vec3`, `WindowProperties`, et `loadPrcFileData` (de `panda3d.core`): Fournissent des fonctionnalités pour la gestion des propriétés de la fenêtre et des configurations 3D.

#### **Classe `Main`**
La classe principale `Main` hérite de `ShowBase` et implémente l'application. 

##### **Attributs principaux**
- `bullet_world`: Instance de `BulletWorld` avec une gravité définie à \( -9.81 \) sur l'axe \( Z \).
- `ui`: Dictionnaire pour gérer les éléments d'interface utilisateur.
- `keys`: Dictionnaire associant des touches du clavier à des fonctions.

##### **Méthodes**
1. **`__init__()`** :
   - Configure la fenêtre (plein écran) et définit les paramètres comme la taille (`1280x720`), le compteur de FPS, et la version OpenGL.
   - Initialise un dictionnaire des touches possibles (`possible_keys`) et lie des événements clavier.

2. **`startup()`** :
   - Lance le menu principal (`MainMenu`) et fournit une méthode pour démarrer le jeu (`start_game`).

3. **`start_game()`** :
   - Instancie une scène de test (`TestWorld`).

4. **`reset()`** :
   - Réinitialise les éléments UI et détache les nœuds de rendu.

5. **`add_key(key, function, args)`** :
   - Ajoute un événement pour une touche donnée et associe une fonction avec ses arguments.

6. **`add_any_key(function)`** :
   - Associe une fonction à toutes les touches possibles.

7. **`on_key_press(key)`** :
   - Appelé lors de la pression d’une touche. Exécute les fonctions associées.

8. **`clear_all_ui()`** :
   - Supprime tous les éléments UI de manière récursive.

##### **Exécution principale**
Si le fichier est exécuté directement :
1. Une instance de `Main` est créée.
2. `startup()` est appelée pour démarrer l'application.
3. La boucle principale de l'application est lancée via `app.run()`.

---

### **Fonctionnalités Clés**
1. **Gestion de la Physique** :
   - Utilisation de `BulletWorld` pour gérer la gravité et d'autres propriétés physiques.
   
2. **Support des Entrées Clavier** :
   - Support complet des touches alphanumériques, des touches spéciales, et des raccourcis clavier (`F1` à `F12`, flèches, etc.).

3. **UI Dynamique** :
   - Les éléments d'interface utilisateur sont gérés de manière centralisée dans le dictionnaire `ui`.

4. **Configuration Personnalisée** :
   - Paramètres graphiques ajustables via `loadPrcFileData`.

---

### **Améliorations Potentielles**
1. **Documentation** :
   - Ajouter des docstrings aux méthodes pour expliquer leur rôle plus en détail.
2. **Gestion des Erreurs** :
   - Raffiner la gestion des exceptions dans `on_key_press` pour inclure des logs plus détaillés.
3. **Optimisation UI** :
   - Introduire un système de gestion UI plus robuste, éventuellement basé sur un framework dédié.
   
# 💡 • Assistance :

### [```Help```](https://github.com/El1teW0lf/2024_2025__p04_projet1_gp1/blob/main/Help.bat) >>> Lancement instantané du projet

Plz help me the owner is so ********
