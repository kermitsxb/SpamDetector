# SpamDetector
Projet Intelligence Artificielle — L3 S6

Au premier push sur le dépot, j'ai simplement suivit le tuto à ce lien : https://docs.djangoproject.com/en/1.9/intro/tutorial01/

## Avancements

Alors j'ai pris le spambase.data, je l'ai exporté au format .csv, ce qui m'a permis d'utiliser le csv reader de python pour parser chaque ligne (chaque email) dans une instance de classe Email (cf. models). Le parser va en fait juste ajouter les 4601 lignes du fichier .csv à la BDD (db.sqlite3) -> les id se rajoutent en auto-increment par défaut.

J'ai rajouter 3 vues et supprimé celle d'accueil pour l'instant: 
	1. url/		-> aucune page HTML encore (j'ai déplacé tout dans le fichier templates à la racine du projet, ce qui est conseillé)
	2. url/email 	-> la BDD des emails (TODO: design HTML/CSS - j'ai inclut bootstrap dans le projet)
	3. url/email/"email_id" 	-> détail de l'email en question
	4. url/email/"email_id"/resultats/		-> pour des résultats approfondis au cas où il la faut (juste pour garder la syntaxe regex si il la faudra)

Voilà maintenant il faut faire la partie graphique du site, les algos, et j'attaque la partie d3js aujourd'hui pour afficher dynamiquement les résultats (écrans) -> d'ailleurs j'ai aucune idée de comment et quoi affiché, donc tenez moi au jus!