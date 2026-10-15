#!/usr/bin/env bash
# Importe un monde Enshrouded local (dossier ou .zip) dans le serveur.
# Usage : ./import-save.sh <dossier-ou-zip> [id-du-monde]
set -euo pipefail

cd "$(dirname "$0")"
SRC="${1:?Usage: $0 <dossier-ou-zip> [id-du-monde]}"
WORLD="${2:-}"
SAVE_DIR=game/server/savegame
SERVER_ID=3ad85aea

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
if [[ "$SRC" == *.zip ]]; then
  unzip -q "$SRC" -d "$TMP" -x "__MACOSX/*"
else
  cp -r "$SRC"/. "$TMP"/
fi

# Liste des mondes présents (fichiers <id>-index)
mapfile -t WORLDS < <(find "$TMP" -type f -name '*-index' -printf '%f\n' | sed 's/-index$//' | sort -u)
if [[ ${#WORLDS[@]} -eq 0 ]]; then
  echo "Aucun monde trouvé (pas de fichier *-index)." >&2; exit 1
fi
if [[ -z "$WORLD" ]]; then
  if [[ ${#WORLDS[@]} -gt 1 ]]; then
    echo "Plusieurs mondes trouvés, précise lequel en 2e argument :" >&2
    for w in "${WORLDS[@]}"; do
      echo "  $w  (modifié le $(date -r "$(find "$TMP" -name "$w-index" | head -1)" '+%F %T'))" >&2
    done
    exit 1
  fi
  WORLD=${WORLDS[0]}
fi
SRC_DIR=$(dirname "$(find "$TMP" -type f -name "$WORLD-index" | head -1)")
echo "Import du monde $WORLD -> $SERVER_ID"

docker compose stop enshrouded

# Hors du dossier backups : le nettoyage automatique n'y garde que les 24 derniers fichiers
mkdir -p sauvegardes-manuelles
BACKUP="sauvegardes-manuelles/avant-import-$(date +%F_%H%M%S).tar.gz"
sudo tar -czf "$BACKUP" -C "$SAVE_DIR" .
echo "Ancienne sauvegarde du serveur : $BACKUP"

sudo find "$SAVE_DIR" -maxdepth 1 -type f \( -name "$SERVER_ID*" -o -name 'world*.ksd' \) -delete
# Enshrouded 1.0 convertit l'ancien format au démarrage : on écarte la conversion précédente
if sudo test -d "$SAVE_DIR/migrated"; then
  sudo mv "$SAVE_DIR/migrated" "$SAVE_DIR/migrated-$(date +%Y%m%d-%H%M%S)"
fi
for f in "$SRC_DIR/$WORLD" "$SRC_DIR/$WORLD"-* "$SRC_DIR/$WORLD"_*; do
  [[ -f "$f" ]] || continue
  name=$(basename "$f")
  sudo cp "$f" "$SAVE_DIR/$SERVER_ID${name#"$WORLD"}"
done
sudo chown -R 1000:1000 "$SAVE_DIR"

docker compose start enshrouded
echo "Terminé. Fichiers importés :"
ls -l "$SAVE_DIR"
