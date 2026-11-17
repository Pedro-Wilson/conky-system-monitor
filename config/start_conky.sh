#!/usr/bin/env bash
# Script para iniciar o Conky e o Monitor Dinâmico de Cores no Zorin OS / XFCE
# Lenovo ThinkPad L440

DELAY=${1:-2}
[ "$DELAY" -gt 0 ] 2>/dev/null && sleep "$DELAY"

# Garante acesso às bibliotecas e binários locais se existirem
[ -d "$HOME/.local/bin" ] && export PATH="$HOME/.local/bin:${PATH}"
[ -d "$HOME/.local/lib/conky/lib" ] && export LD_LIBRARY_PATH="$HOME/.local/lib/conky/lib:${LD_LIBRARY_PATH}"

CONFIG_DIR="${HOME}/.config/conky"
CONFIG_FILE="$CONFIG_DIR/conky.conf"
THEME_SCRIPT="$CONFIG_DIR/scripts/wallpaper_theme.py"
MONITOR_SCRIPT="$CONFIG_DIR/scripts/wallpaper_monitor.py"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Erro: Arquivo de configuração $CONFIG_FILE não encontrado." >&2
    exit 1
fi

# Aplica as cores em contraste com o wallpaper atual antes de exibir
if [ -x "$THEME_SCRIPT" ]; then
    python3 "$THEME_SCRIPT" --apply >/dev/null 2>&1
fi

# Evita processos duplicados do Conky
pkill -u "$USER" -x conky 2>/dev/null
sleep 0.3

# Localiza binário do Conky (local ou do sistema)
CONKY_BIN="conky"
if [ -x "$HOME/.local/bin/conky" ]; then
    CONKY_BIN="$HOME/.local/bin/conky"
fi

# Inicia o Conky desvinculado de sessão de terminal (setsid)
setsid -f "$CONKY_BIN" -c "$CONFIG_FILE" >/dev/null 2>&1
sleep 0.8

# Inicia o daemon monitor de wallpaper em background (se já não estiver rodando)
if [ -x "$MONITOR_SCRIPT" ]; then
    if ! pgrep -u "$USER" -f "wallpaper_monitor.py" >/dev/null; then
        setsid -f python3 "$MONITOR_SCRIPT" >/dev/null 2>&1
    fi
fi

# Valida se subiu com sucesso
if pgrep -u "$USER" -x conky >/dev/null; then
    echo "Conky e Monitor de Cores iniciados com sucesso (PID: $(pgrep -u "$USER" -x conky | tr '\n' ' '))."
    exit 0
else
    echo "Falha ao iniciar o Conky." >&2
    exit 1
fi
