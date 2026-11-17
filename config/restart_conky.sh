#!/usr/bin/env bash
# Script para reiniciar o Conky

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/stop_conky.sh"
sleep 1
"$SCRIPT_DIR/start_conky.sh" 0
