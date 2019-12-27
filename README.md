# Intoduction / contexte

Projet de compilateur du 5ème semestre de Bachelor à la Haute-Ecole Arc.

Année 2019-2020.

## Auteurs

François Bouthillier de Beaumont, Romain Capocasale, Jonas Freiburghaus

# Cahier des charges

Le but de projet est de créer un language et de le compiler vers du JavaScript, afin de pouvoir dessiner instictivement sur un canvas HTML. Ainsi, grâce à une syntaxe très lisible, l'utilisateur du langague aurait la possibilité de créer des acteurs, les tortues, et de les déplacer sur le canvas.
Un acteur (Tortue) a une position X, une position Y et un sens.
Une tortue fait partie d'une zone (Galapagos) et ne peut en sortir. Elle peut se déplacer en avant et en arrière, et peut tourner sur elle même.
Selon la volonté de l'utilisateur, une tortue dessine derrière elle ou non.

Le compilateur devra aussi verifier que l'utilisateur n'effectue pas d'opération illégale. Les opérations considérés comme illégales sont :

 * Deux tortues ne peuvent entrer en collision.
 * Une tortue ne peut sortir de sa zone (Galapagos).


Si de tel cas se produisent, le compilateur lancera une erreur.

Le langage doit être compilé au travers des étapes suivantes :

* Analyse lexicale
* Analyse syntaxique
* Analyse sémantique
* Génération de code

## Objectifs principaux

Notre language permettra la compilation vers du Javascript et offrira les possibilités suivantes:
   * Initialisation d'acteurs
   * Déplacement et rotation d'acteurs
   * Initialisation de zones liées aux acteurs
   * Tracé (ou non) derrière les acteurs
   * Opérations illégales:
      * Impossibilité de mener des acteurs en dehors de leur zone
      * Impossibilité de mener des acteurs à une collision

# Fonctionnement du langage

## Fonctionnalités

* Variables
* Branchement
* Boucle
* Fonctions préfaites
* Commentaire uniligne
* Evaluation algébrique

## Mots clés réservés

* **Tortue < nom > = < Galapagos >, < positionX >, < positionY >, < angle >;**
<br/>Crée une nouvelle tortue dans la zone <Galapagos>, en position <positionX>;<postionY> et d'angle <angle>. Les angles suivent la logique d'un cercle trigonométrique.
* **Galapagos < nom > = < positionX >, < positionY >, < width >, < height >;**
<br/>Créer une zone dans laquelle peut se déplacer une ou plusieurs tortue
* **Avancer < tortue > < distance >;**
<br/>Fait avancer une <tortue> d'une certaine <distance>
* **Reculer < tortue > < distance >;**
<br/>Fait reculer une <tortue> d'une certaine <distance>
* **TournerGauche < tortue > < angle >;**
<br/>Fait tourner la tortue dans le sens antihoraire
* **TournerDroite < tortue > < angle >;**
<br/>Fait tourner la tortue dans le sens horaire
* **Decoller < tortue >;**
<br/>La Tortue ne dessine plus son tracé derrière elle
* **Atterrir < tortue >;**
<br/>La Tortue dessine le tracé derrière elle
* **Si < condition > { < programme > }**
<br/><programme> est executé uniquement si <condition> est satisfait
* **Tq < condition > { < programme > }**
<br/><programme> est executé tant que <condition> est satisfait
* **positionX(< tortue >)**
<br/>Retourne la position actuelle de la tortue sur l'axe X
* **positionY(< tortue >)**
<br/>Retourne la position actuelle de la tortue sur l'axe Y
* **// < texte >**
<br/>Commentaire

## Régles de gramaire

* **programme : statement ';' **
* **programme : statement ';' programme**
* **statement : assignation
       | structure**
* **structure : TQ expression '{' programme '}'**
* **structure : SI expression '{' programme '}'**
* **expression : expression ALGEBRAIC_OP expression**
* **expression : NUMBER
        | IDENTIFIER**
* **assignation : IDENTIFIER '=' expression**
* **assignation : ENTIER IDENTIFIER '=' expression
        | GALAPAGOS IDENTIFIER '=' expression expression expression expression
        | TORTUE IDENTIFIER '=' expression expression expression expression**
* **statement : AVANCER expression expression**
* **statement : RECULER expression expression**
* **statement : TOURNERGAUCHE expression expression**
* **statement : TOURNERDROITE expression expression**
* **statement : DECOLLER expression**
* **statement : ATTERRIR expression**
* **expression : POSITIONX '(' expression ')'**
* **expression : POSITIONY '(' expression ')'**

## Conventions

* [x] Les mots clés réservés sont en PascalCase
* [x] Les fichiers contenant du code Galapagos ont l'extension .galapagos
* [x] Indentation de style Allman
* [x] Code en français

"Les conventions dans le langage Galapagos ne sont pas obligatoires, mais vivement recommandées pour la maintenance et le travail en équipe."

-- <cite>Bouthiller de Beaumont, Capocasale, Freiburghaus: Galapagos in a turtle shell</cite>

## Exemple de script

```galapagos
Galapagos g = 0, 10, 50, 50;  // Definis une zone pour une tortue
Tortue t = g, 10,10, 0; // Cree une tortue dans la zone g

Avancer t 10;
Reculer t 10;
TournerGauche t 10;
TournerDroite t 30;
Decoller t;
Atterrir t;

Si positionX(t) > 10
{
    TournerGauche g 10;
};

Tq positionY(t) < 20
{
    Avancer t 10;
};
```

# Historique des changements

* positionX t -> positionX(t)
* positionY t -> postionY(t)

# Spécificité du language
* Mettre ici tout les fonctionnalités unique à notre projet

## Partie Avant
### Analyse sémantique
## Partie Arrière
###  Génération de code
Notre programme génére du code javascript à partir de l'arbre syntaxique en entré. Dans le fichier du compilateur, une fonction corresponds à un noeud de l'arbre. La fonction génére du code javascript selon le type de noeud. La génération du code est effectué de manière récursive en partant du bas de l'arbre. Les noeuds en bas de l'arbre sont exécuté et remonte petit à petit en haut de l'arbre.

Le code est généré dans le fichier ``outputs/compiled_code.js``. En plus du code provenant de l'arbre, ce fichier contient également du code javascript supplémentaire pour faire le lien avec le canvas HTML et pour les animations. Lors de la compilation, le compilateur va directement utilsé des objets javascript défini au préalable dans ``outputs/galapagos_lib/js``. Dans ce dossier se trouve plusieurs fichiers javascript définissant différentes classes. Ces classes représente nottamment une tortue et un galapagos (au sens javascript) et permettent d'effectuer des actions avec ces objets.

Le code résultant de la compilation doit donc être executé dans une page HTML. Dans le dossier ``outputs/`` se trouve également un fichier ``Galapagos.html`` qui va exécuté le code se trouvant dans ``compiled_code.js``. Normalement le fichier ``Galapagos.html`` s'ouvre automatiquement à la fin de la compilation.

### Animation
Lors de la génération de code, les différents déplacement de la tortue sont déposés dans une queue (coté javascript). Une fois le fichier ``Galapagos.html`` lancé, les animations dans la queue vont être exécuté dans l'ordre une par une. Un interval fixe est défini entre chaque exécution d'un mouvement de la tortue. Ceci pour donner un effet d'animation.

# Conclusion

## TODO

* [ ] Raise error when syntax fails
* [ ] Add ligne error *Kinda done, check method p_error(p) in g_parser.py*
* [ ] Do we deal with floats ?
  * If yes: _Avancer t 10.2_ should not raise an error_ (not like now)
  * If no: _Avancer t 10. should raise an error_ (not like now)
