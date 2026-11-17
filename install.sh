#!/usr/bin/env bash
# ==============================================================================
# Installer Script for Conky System Monitor (ThinkPad HUD)
# ==============================================================================

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.config/conky"
AUTOSTART_DIR="${HOME}/.config/autostart"

echo "=================================================="
echo "  Instalação do Conky System Monitor"
echo "=================================================="

# 1. Checagem de dependências
echo "[+] Verificando dependências..."
MISSING_PKGS=()

command -v conky >/dev/null 2>&1 || [ -x "$HOME/.local/bin/conky" ] || MISSING_PKGS+=("conky-all")
command -v python3 >/dev/null 2>&1 || MISSING_PKGS+=("python3")
python3 -c "import PIL" >/dev/null 2>&1 || MISSING_PKGS+=("python3-pil")
command -v xfconf-query >/dev/null 2>&1 || MISSING_PKGS+=("xfconf")
command -v lm-sensors >/dev/null 2>&1 || command -v sensors >/dev/null 2>&1 || MISSING_PKGS+=("lm-sensors")

if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
    echo "[-] Dependências ausentes detectadas: ${MISSING_PKGS[*]}"
    echo "    Recomendado executar: sudo apt update && sudo apt install -y ${MISSING_PKGS[*]}"
else
    echo "[✓] Todas as dependências principais estão presentes."
fi

# 2. Criar diretórios de destino
echo "[+] Criando diretórios em ~/.config..."
mkdir -p "$TARGET_DIR/scripts"
mkdir -p "$AUTOSTART_DIR"

# 3. Copiar arquivos de configuração e scripts
echo "[+] Copiando arquivos de configuração..."
cp -r "$REPO_DIR/config/"* "$TARGET_DIR/"
chmod +x "$TARGET_DIR"/*.sh
chmod +x "$TARGET_DIR/scripts"/*.sh
chmod +x "$TARGET_DIR/scripts"/*.py

# 4. Configurar Autostart
echo "[+] Configurando inicialização automática..."
cp "$REPO_DIR/autostart/conky.desktop" "$AUTOSTART_DIR/conky.desktop"
chmod +x "$AUTOSTART_DIR/conky.desktop"

# 5. Iniciar Conky
echo "[+] Iniciando o Conky e o monitor de wallpaper..."
"$TARGET_DIR/start_conky.sh" 1

echo "=================================================="
echo "[✓] Conky System Monitor instalado com sucesso!"
echo "    Configuração: ~/.config/conky/conky.conf"
echo "    Para reiniciar: ~/.config/conky/restart_conky.sh"
echo "    Para alternar modo: python3 ~/.config/conky/scripts/wallpaper_theme.py --matrix | --dynamic"
echo "=================================================="
