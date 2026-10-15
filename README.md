# Serveur dédié Enshrouded

Configuration Docker d'un serveur dédié [Enshrouded](https://store.steampowered.com/app/1203620/Enshrouded/) (4 joueurs), basée sur l'image [`mornedhels/enshrouded-server`](https://github.com/mornedhels/enshrouded-server), avec mises à jour et sauvegardes automatiques, et notifications Discord.

## Contenu

| Fichier | Rôle |
|---|---|
| `docker-compose.yml` | Le conteneur du serveur : image Wine, rôles Admin / Amis, mises à jour toutes les 30 min, sauvegardes toutes les 2 h (24 gardées) |
| `patches/enshrouded-backup` | Script de sauvegarde corrigé pour le format de sauvegarde d'Enshrouded 1.0 (PR upstream #256), monté dans le conteneur. À retirer quand l'image l'intégrera |
| `import-save.sh` | Importe un monde local (dossier ou `.zip`) dans le serveur, après avoir archivé le monde actuel dans `sauvegardes-manuelles/` |
| `discord-notifier.py`, `enshrouded-discord.service` | Lit les logs et événements Docker du conteneur et poste sur un webhook Discord : arrivées/départs, démarrage, arrêt, plantage, RAM presque pleine. Tourne comme service systemd |
| `CONNEXION.md` | Guide pour les joueurs : rejoindre le serveur |
| `BOT-DISCORD.md` | Documentation du bot Discord (le code du bot est dans un autre dossier, `~/enshrouded-bot/`) |
| `DISCORD-MESSAGES.md` | Messages prêts à coller dans le salon Discord |
| `bot-icon.svg` / `bot-icon.png` | Icône du bot |

Non versionnés (voir `.gitignore`) : `.env`, le dossier `game/` (binaires, monde, logs : plusieurs Go) et `sauvegardes-manuelles/`.

## Installation

Prérequis : Docker avec le plugin Compose, et un noyau qui expose `/dev/ntsync` (utilisé par Wine).

1. Créer le fichier `.env` :

   ```env
   SERVER_NAME=Mon serveur Enshrouded
   ADMIN_PASSWORD=un-mot-de-passe-admin
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
   ```

2. Démarrer le serveur :

   ```bash
   docker compose up -d
   ```

   Au premier lancement, le jeu est téléchargé dans `game/`. Le mot de passe du rôle « Amis » et la difficulté se règlent ensuite dans `game/server/enshrouded_server.json`.

3. Ouvrir le port **15637/UDP** dans le pare-feu.

## Notifications Discord

`discord-notifier.py` lit `DISCORD_WEBHOOK_URL` dans `.env`. Sur le VPS, il tourne comme service systemd, avec l'unité fournie :

```bash
sudo cp enshrouded-discord.service /etc/systemd/system/
sudo systemctl enable --now enshrouded-discord
```

## Importer un monde

```bash
./import-save.sh ~/MonMonde.zip
```

S'il y a plusieurs mondes dans l'archive, le script les liste ; passer l'identifiant voulu en deuxième argument. Le serveur est arrêté pendant l'import, puis redémarré.

## Notes

- L'image utilise la variante **Wine** (`1.7.2-wine`) : la variante Proton (`latest`) ne démarre pas avec Enshrouded 1.0.
- La mémoire du conteneur est limitée à 6 Go.
