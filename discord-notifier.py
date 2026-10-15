#!/usr/bin/env python3
"""Lit les logs du conteneur Enshrouded et poste les événements sur un webhook Discord."""
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

CONTAINER = "enshrouded"
ENV_FILE = Path(__file__).with_name(".env")
RAM_ALERT_RATIO = 0.90
RAM_ALERT_COOLDOWN = 30 * 60

GREEN, RED, BLUE, ORANGE, GREY = 0x2ECC71, 0xE74C3C, 0x3498DB, 0xE67E22, 0x95A5A6


def load_env():
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = load_env()
WEBHOOK = ENV.get("DISCORD_WEBHOOK_URL") or sys.exit("DISCORD_WEBHOOK_URL manquant dans .env")
SLOTS = 4
players = set()
lock = threading.Lock()
stopping = False  # arrêt volontaire en cours (pas un crash)


def send(title, color, description=None):
    embed = {"title": title, "color": color}
    if description:
        embed["description"] = description
    body = json.dumps({"username": "Enshrouded", "embeds": [embed]}).encode()
    req = urllib.request.Request(
        WEBHOOK, data=body,
        headers={"Content-Type": "application/json", "User-Agent": "enshrouded-notifier/1.0"},
    )
    for _ in range(3):
        try:
            urllib.request.urlopen(req, timeout=10).close()
            return
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(float(e.headers.get("Retry-After", 2)))
                continue
            print(f"webhook HTTP {e.code}: {e.read()[:200]}", flush=True)
            return
        except Exception as e:
            print(f"webhook erreur: {e}", flush=True)
            time.sleep(2)


def count():
    return f"{len(players)}/{SLOTS} joueurs connectés"


def handle(line):
    global stopping
    if m := re.search(r"\[server\] Player '(.+?)' logged in", line):
        with lock:
            players.add(m[1])
        send(f"👋 {m[1]} a rejoint la partie", GREEN, count())
    elif m := re.search(r"\[server\] Remove Player '(.+?)'", line):
        with lock:
            players.discard(m[1])
        send(f"🚪 {m[1]} a quitté la partie", GREY, count())
    elif "'HostOnline' (up)" in line:
        stopping = False
        with lock:
            players.clear()
        send("🟢 Serveur en ligne", GREEN, "`51.75.204.124:15637`")
    elif "Shutting down enshrouded server" in line or "Stopping enshrouded server" in line:
        if not stopping:
            stopping = True
            send("🔴 Serveur arrêté", RED)
    elif "Enshrouded server needs to be updated" in line:
        send("🔄 Mise à jour du jeu en cours", BLUE, "Le serveur redémarre dans quelques minutes.")
    elif "enshrouded-backup complete" in line:
        send("💾 Sauvegarde effectuée", GREY)


def follow_logs():
    since = str(int(time.time()))
    last_ts = ""
    while True:
        proc = subprocess.Popen(
            ["docker", "logs", "-f", "--timestamps", "--since", since, CONTAINER],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace",
        )
        for line in proc.stdout:
            ts = line.split(" ", 1)[0]
            if ts <= last_ts:  # déjà traité avant la reconnexion
                continue
            since = last_ts = ts
            try:
                handle(line)
            except Exception as e:
                print(f"erreur sur la ligne {line!r}: {e}", flush=True)
        proc.wait()
        # le flux se coupe quand le conteneur s'arrête : on attend et on se reconnecte
        time.sleep(5)


def watch_events():
    global stopping
    while True:
        proc = subprocess.Popen(
            ["docker", "events", "--filter", f"container={CONTAINER}",
             "--filter", "event=die", "--filter", "event=oom", "--format", "{{json .}}"],
            stdout=subprocess.PIPE, text=True,
        )
        for line in proc.stdout:
            ev = json.loads(line)
            if ev.get("status") == "oom" or ev.get("Action") == "oom":
                send("💥 Le serveur a manqué de mémoire", RED, "Il va redémarrer automatiquement.")
            elif ev["Actor"]["Attributes"].get("exitCode", "0") != "0" and not stopping:
                send("⚠️ Le serveur a planté", RED,
                     f"Code de sortie {ev['Actor']['Attributes']['exitCode']}. Redémarrage automatique en cours.")
            with lock:
                players.clear()
        proc.wait()
        time.sleep(5)


def watch_ram():
    last_alert = 0
    while True:
        time.sleep(60)
        out = subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "{{.MemPerc}}", CONTAINER],
            capture_output=True, text=True,
        ).stdout.strip().rstrip("%")
        try:
            ratio = float(out) / 100
        except ValueError:
            continue
        if ratio >= RAM_ALERT_RATIO and time.time() - last_alert > RAM_ALERT_COOLDOWN:
            last_alert = time.time()
            send("⚠️ Mémoire presque pleine", ORANGE, f"Le serveur utilise {ratio:.0%} de sa limite de RAM.")


if __name__ == "__main__":
    threading.Thread(target=watch_events, daemon=True).start()
    threading.Thread(target=watch_ram, daemon=True).start()
    print("notifier démarré", flush=True)
    follow_logs()
