# Le bot Discord Enshrouded

Le bot **Enshrouded** est présent sur le Discord *La Guilde*. Il suit le serveur en permanence et répond à des commandes dans le salon **#🏰enshrouded**.

## Ce qu'il fait tout seul

- **Statut dans la liste des membres** : « Joue à Enshrouded — 2/4 joueurs ».
  - 🟢 vert : le serveur est en ligne
  - 🟡 jaune : il démarre ou se met à jour
  - 🔴 rouge : il est arrêté
- **Message épinglé** dans #🏰enshrouded, mis à jour toutes les minutes :
  - l'état du serveur et l'adresse
  - les joueurs connectés, et depuis combien de temps
  - depuis quand le serveur est en ligne, et la RAM utilisée
- **Annonces automatiques** dans le salon :
  - 👋 *zlatizer a rejoint la partie (1/4)*
  - 🚪 *zlatizer est parti après 2 h 15*
  - 🟢 serveur en ligne / 🔴 serveur arrêté
  - ⏳ mise à jour du jeu disponible mais en attente : elle s'installe quand tout le monde est déconnecté
  - 🔄 mise à jour du jeu en cours, ou ⚠️ échouée
  - 💾 sauvegarde automatique effectuée (toutes les 2 h)
  - 💥 plantage, avec la cause probable quand elle est connue
  - 🛑 le serveur n'arrive plus à démarrer (une seule alerte par panne)
  - ⚠️ mémoire presque pleine (plus de 90 % de la limite)
- 🏅 **Succès** débloqués par les joueurs : 10 / 50 / 100 / 250 heures, Marathon (4 h d'affilée), Couche-tard (en jeu à 3 h), Lève-tôt (connecté entre 5 h et 8 h), Premier arrivé de la semaine, Assidu (5 jours dans la semaine), Escouade complète (serveur plein).
- 📝 **Notes de mise à jour officielles** postées automatiquement quand Enshrouded publie un correctif.
- 🌙 **Redémarrage nocturne** vers 5 h, seulement si personne ne joue, pour libérer la RAM. Une seule annonce discrète, avec la RAM avant/après.
- **Résumé de la semaine**, chaque dimanche à 20 h : temps de jeu total (et comparaison avec la semaine d'avant), sessions, classement, record de joueurs connectés en même temps, jour le plus actif, nouveaux joueurs.

Les annonces sont encadrées avec une couleur selon le type : 🟩 vert pour les arrivées et la mise en ligne, ⬜ gris pour les départs et les sauvegardes, 🟦 bleu pour les mises à jour, 🟧 orange pour les avertissements, 🟥 rouge pour les arrêts et les pannes.

## Utiliser une commande

Dans #🏰enshrouded, tape `/` : la liste des commandes du bot s'affiche. Choisis-en une et appuie sur **Entrée**.

Les réponses sont **privées** : toi seul les vois (mention *« Seul·e toi peux voir ce message »*). Tu ne pollues donc pas le salon.

## Commandes pour tout le monde

| Commande | Ce qu'elle fait |
|---|---|
| `/aide` | Liste toutes les commandes du bot |
| `/status` | État du serveur : en ligne ou non, joueurs connectés, RAM |
| `/joueurs` | Joueurs connectés + classement 🥇🥈🥉 du temps de jeu total |
| `/connexion` | Nom, adresse et mot de passe du serveur, avec les étapes pour rejoindre. Le mot de passe est masqué : clique dessus pour l'afficher |
| `/historique` | Les 15 dernières sessions de jeu (qui, quand, combien de temps) |
| `/stats` | Temps de jeu cumulé, nombre de sessions, record de joueurs connectés en même temps, joueur de la semaine 🏆 |
| `/resume` | Le résumé des 7 derniers jours, à tout moment |
| `/profil [joueur]` | La fiche d'un joueur : temps de jeu (total et semaine), sessions, record, classement, dernière et première connexion, créneau préféré, succès. Sans joueur : ta fiche (après `/lier`) |
| `/vu <joueur>` | Quand le joueur était là pour la dernière fois, et combien de temps |
| `/activite` | Graphique : quand le groupe joue (jour × heure sur 30 jours) et temps de jeu par jour sur 14 jours |
| `/version` | Version installée sur le serveur, dernière version sur Steam, et si une mise à jour est en attente |
| `/patchnotes` | Les dernières notes de mise à jour officielles (option `publier` pour les poster dans le salon) |
| `/lier <pseudo>` | Relie ton pseudo en jeu à ton compte Discord : tu es cité dans les annonces, `/profil` marche sans argument, et tu reçois le rôle 🎮 *En jeu* pendant la partie. `/delier` pour retirer |
| `/session` | Propose une session (jour, heure, note) avec boutons ✅ Je viens / 🤔 Peut-être / ❌ Pas dispo. Le bot crée un événement Discord et envoie un rappel 15 min avant en mentionnant les inscrits. L'organisateur ou un admin peut l'annuler |
| `/dispo` | Coche tes soirs libres des 7 prochains jours ; le bot affiche le meilleur soir. Option `publier` pour poster le tableau |
| `/alerte` | Être mentionné : 🎮 quand quelqu'un lance une partie (serveur vide → 1 joueur), 👋 à chaque connexion, ou 🟢 quand le serveur revient après une panne. Refais la même commande pour désactiver. Sans option : affiche tes alertes |

## Commandes admin

Ces commandes ne sont visibles et utilisables que par les **administrateurs** du Discord.

Les commandes qui coupent le serveur (`/restart`, `/maj`, `/restaurer`) demandent toujours une **confirmation par bouton**. Si des joueurs sont connectés, le message de confirmation les liste, car ils seront déconnectés. Le bot annonce aussi dans le salon qui a lancé l'opération.

| Commande | Ce qu'elle fait |
|---|---|
| `/restart` | Redémarre le serveur. Il revient en ligne en 1 à 3 minutes |
| `/maj` | Redémarre le serveur en installant la dernière version du jeu, s'il y en a une. Pratique quand le jeu vient d'être mis à jour sur Steam et que les joueurs ont une erreur de version |
| `/backup` | Sauvegarde immédiate du monde, sans couper le serveur. À faire avant un gros chantier ou un boss |
| `/sauvegardes` | Liste les sauvegardes disponibles, avec leur date et leur taille |
| `/restaurer` | Remet le monde dans l'état d'une sauvegarde (voir ci-dessous) |
| `/exporter` | Télécharge une copie du monde (fichier ZIP), à garder ailleurs que sur le VPS |
| `/motdepasse [nouveau]` | Change le mot de passe des joueurs (généré si vide), redémarre le serveur, et annonce de taper `/connexion` |
| `/difficulte [preset]` | Affiche la difficulté, ou passe en Relaxed / Default / Hard / Survival (redémarrage) |
| `/vps` | État du VPS : RAM, swap, disque, charge CPU, temps allumé, + graphique de la RAM du serveur sur 24 h |
| `/logs` | Affiche les dernières lignes des logs du serveur, pour diagnostiquer un problème. Option `lignes` : de 5 à 50 (20 par défaut) |

### Restaurer une sauvegarde

1. Tape `/restaurer`. Une liste des sauvegardes apparaît, la plus récente en premier.
2. Choisis la sauvegarde. Tu peux taper une date pour filtrer, par ex. `10-14`.
3. Le bot rappelle la date de la sauvegarde et prévient que tout ce qui a été fait depuis sera perdu. Clique sur **Restaurer** pour confirmer.
4. Le serveur s'arrête, le monde est remplacé, puis le serveur redémarre.

L'état du monde juste avant la restauration est gardé dans une sauvegarde `…-avant-restauration.zip`. Tu peux donc annuler une restauration en restaurant ce fichier.

### Les sauvegardes

- **Automatiques** : toutes les 2 heures. Les 24 plus récentes sont gardées, soit 2 jours d'historique.
- **Manuelles** : avec `/backup`. Elles sont nommées `…-manuel.zip`.
- Une sauvegarde ne contient que le **monde** (constructions, coffres, carte). Les **personnages** sont sauvegardés sur le PC de chaque joueur et ne sont pas touchés par une restauration.

## Ce que le bot ne peut pas faire

Enshrouded n'a pas de console d'administration à distance. Ces actions se font **en jeu** uniquement :

- exclure ou bannir un joueur ;
- envoyer un message dans le chat du jeu ;
- changer l'heure, la météo ou la difficulté.

## Pour l'admin du VPS

- Les fichiers du bot sont dans `~/enshrouded-bot/`. La configuration est dans `.env` et `docker-compose.yml`.
- **Donner les commandes admin à un rôle** sans le rendre administrateur :
  1. Mets l'identifiant du rôle dans `ADMIN_ROLE_ID=` du fichier `.env`.
  2. Relance le bot avec `docker compose up -d` (dans `~/enshrouded-bot/`).
  3. Dans Discord, va dans **Paramètres du serveur → Intégrations → Enshrouded** et autorise ce rôle pour les commandes admin.
- **Copie quotidienne du monde hors du VPS** : mets l'identifiant d'un salon privé (visible seulement par les admins et le bot) dans `BACKUP_CHANNEL_ID=` du fichier `.env`. Le bot y enverra chaque jour à 5 h le ZIP du monde. Sans ce réglage, utilise `/exporter`.
- **Rôle 🎮 En jeu** : crée un rôle « En jeu », place-le **sous** le rôle du bot *Enshrouded* (Paramètres du serveur → Rôles, glisser-déposer), donne au rôle du bot la permission **Gérer les rôles**, puis mets l'identifiant du rôle dans `INGAME_ROLE_ID=` du fichier `.env`.
- **Redémarrage nocturne** : heure dans `NIGHTLY_RESTART_HOUR=` (5 par défaut, `-1` pour désactiver).
- **Mot de passe et difficulté** : ils sont stockés dans `~/enshrouded-server/game/server/enshrouded_server.json` (plus dans `docker-compose.yml`), modifiés par `/motdepasse` et `/difficulte`.
- **Désactiver les annonces** : ajoute `ANNOUNCE=false` dans `.env`, puis relance le bot. Pour couper seulement les annonces de sauvegarde : `ANNOUNCE_BACKUPS=false`.
- **Voir les logs du bot** :
  ```bash
  docker logs -f enshrouded-bot
  ```
- **Sécurité** : le bot passe par un proxy Docker qui ne l'autorise qu'à lire, arrêter, démarrer et redémarrer le conteneur `enshrouded`. Tout le reste est refusé. Les règles sont dans `haproxy.cfg.template`.
