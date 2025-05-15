#!/bin/bash

echo "[ENTRYPOINT] Génération du config.json à partir de .env..."

export $(grep -v '^#' /freqtrade/.env | xargs -d '\n')


envsubst < /freqtrade/user_data/config.json.template > /freqtrade/user_data/config.json

echo "[ENTRYPOINT] Lancement du bot Freqtrade..."
freqtrade "$@"

