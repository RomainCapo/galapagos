# Galapagos

Projet de compilateur du 5ème semestre de Bachelor à la Haute-Ecole Arc.

Année 2019-2020.

## Auteurs

François Bouthillier de Beaumont, Romain Capocasale, Jonas Freiburghaus

## Cahier des charges
Le but de projet est de créer un language et de le compiler vers du JavaScript, afin de pouvoir dessiner instictivement sur un canvas HTML. Ainsi, grâce à une syntaxe très lisible, l'utilisateur du langague aurait la possibilité de créer des acteurs, les tortues, et de les déplacer sur le canvas.
Un acteur (Tortue) a une position X, une position Y et un sens.
Une tortue fait partie d'une zone (Galapagos) et ne peut en sortir. Elle peut se déplacer en avant et en arrière, et peut tourner sur elle même.
Selon la volonté de l'utilisateur, une tortue dessine derrière elle ou non.

Le compilateur devra aussi verifier que l'utilisateur n'effectue pas d'opération illégale. Les opérations considérés comme illégales sont :

 * Deux tortues ne peuvent entrer en collision.
 * Une tortue ne peut sortir de sa zone (Galapagos).


Si de tel cas se produise, le compilateur lancera une erreur.

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

## Fonctionnement du langage

### Fonctionnalités

* Variables
* Branchement
* Boucle
* Fonctions préfaites
* Commentaires uniligne
* (Evaluation algébrique)


### Mots clés réservés

* **Tortue < nom > = < Galapagos >, < positionX >, < positionY >, < angle >;**
<br/>Crée une nouvelle tortue dans la zone <Galapagos>, en position <positionX>;<postionY> et d'angle <angle>. Les angles suivent la logique d'un cercle trigonométrique.
* **Galapagos < nom > = < positionX >, < positionY >, < width >, < height >;**
<br/>Créer une zone dans laquelle peut se déplacer une ou plusieurs tortue
* **Avancer < tortue > < quantité >;**
<br/>Fait avancer une <tortue> d'une certaine <quantité>
* **Reculer < tortue > < quantité >;**
<br/>Fait reculer une <tortue> d'une certaine <quantité>
* **TournerGauche < tortue > < angle >;**
<br/>Fait tourner la tortue dans le sens antihoraire
* **TournerDroite < tortue > < angle >;**
<br/>Fait tourner la tortue dans le sen horaire
* **Decoller < tortue >;**
<br/>La Tortue ne dessine plus son tracé derrière elle
* **Atterrir < tortue >;**
<br/>La Tortue dessine le tracé derrière elle
* **Si < condition > { < instruction > }**
<br/><instruction> est executé uniquement si <condition> est satisfait
* **Tq < condition > { < instruction > }**
<br/><instruction> est executé tant que <condition> est satisfait
* **positionX < tortue >**
<br/>Retourne la position actuelle de la tortue sur l'axe X
* **positionY < tortue >**
<br/>Retourne la position actuelle de la tortue sur l'axe Y
* **§§ < texte >**
<br/>Commentaire

### Gramaire

* **expression : NUMBER | IDENTIFIER**
* **expression : expression COMPARISON_OP expression**
* **assignation : IDENTIFIER '=' expression
  | GALAPAGOS IDENTIFIER '=' expression ',' expression ',' expression ',' expression
  | TORTUE IDENTIFIER '=' expression ',' expression ',' expression ',' expression**
* **programme : statement ';' programme**
* **programme : statement ';'**
* **structure : TQ expression '{' programme '}'**
* **statement : assignation | structure**

### Conventions

* [x] Les mots clés réservés sont en PascalCase
* [x] Les fichiers contenant du code Galapagos ont l'extension .galapagos
* [x] Indentation de style Allman
* [x] Code en français

"Les conventions dans le langage Galapagos ne sont pas obligatoires, mais vivement recommandées pour la maintenance et le travail en équipe."

-- <cite>Bouthiller de Beaumont, Capocasale, Freiburghaus: Galapagos in a turtle shell</cite>

### Exemple de script

```galapagos
Galapagos g = 0, 10, 50, 50;  §§ Definis une zone pour une tortue
Tortue t = g, 10,10, 0; §§ Cree une tortue dans la zone g

Avancer t 10;
Reculer t 10;
TournerGauche t 10;
TournerDroite t 30;
Decoller t;
Atterrir t;

Si positionX t > 10
{
    TournerGauche g 10;
};

Tq positionY t < 20
{
    Avancer t 10;
};
```

## TODO

* [.] Raise error when syntax fails
