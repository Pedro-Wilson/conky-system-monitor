#!/usr/bin/env bash
# ==============================================================================
# Uninstaller Script for Conky System Monitor
# ==============================================================================

TARGET_DIR="${HOME}/.config/conky"
AUTOSTART_FILE="${HOME}/.config/autostart/conky.desktop"

echo "=================================================="
echo "  Desinstalação do Conky System Monitor"
echo "=================================================="

# Parar serviços
if [ -f "$TARGET_DIR/stop_conky.sh" ]; then
    echo "[+] Parando processos do Conky..."
    "$TARGET_DIR/stop_conky.sh"
else
    pkill -u "$USER" -f "wallpaper_monitor.py" 2>/dev/null
    pkill -u "$USER" -x conky 2>/dev/null
fi

# Remover autostart
if [ -f "$AUTOSTART_FILE" ]; then
    echo "[+] Removendo inicialização automática..."
    rm -f "$AUTOSTART_FILE"
fi

# Remover diretório de configuração
read -r -p "Deseja remover as configurações em $TARGET_DIR? (s/N): " response
case "$response" in
    [sS][iI][mM]|[sS])
        rm -rf "$TARGET_DIR"
        echo "[✓] Configurações removidas com sucesso."
        ;;
    *)
        echo "[*] Configurações mantidas em $TARGET_DIR."
        ;;
esac

echo "=================================================="
echo "[✓] Desinstalação concluída."
echo "=================================================="
