#!/usr/bin/env bash
# Script para finalizar o Conky e o Monitor Dinâmico de Cores

# Finaliza o daemon do wallpaper monitor
pkill -u "$USER" -f "wallpaper_monitor.py" 2>/dev/null
PID_FILE="${HOME}/.config/conky/.wallpaper_monitor.pid"
[ -f "$PID_FILE" ] && rm -f "$PID_FILE"

# Finaliza o Conky
pkill -u "$USER" -x conky 2>/dev/null
sleep 0.5

if pgrep -u "$USER" -x conky >/dev/null; then
    pkill -9 -u "$USER" -x conky 2>/dev/null
fi

echo "Conky e Monitor de Cores finalizados."
