# Conky System Monitor HUD

Painel de monitoramento do sistema minimalista e moderno em estilo HUD para desktop Linux (XFCE / Zorin OS / Ubuntu).

## Recursos

- **Monitoramento em tempo real**:
  - Relógio digital e data.
  - CPU: modelo, frequência em GHz, uso total e temperatura por núcleo.
  - Memória: RAM usada/total e memória Swap com barras gráficas.
  - GPU: identificação da GPU Intel e frequência de operação.
  - Disco: consumo da partição raiz e espaço livre.
  - Rede: detecção automática de interface ativa (Ethernet ou Wi-Fi), velocidade de upload/download e histórico em gráfico.
  - Processos: top processos por consumo de CPU e Memória RAM.
- **Cores Dinâmicas & Modo Matrix**:
  - **Modo Dynamic**: analisa a luminosidade e paleta do papel de parede ativo e adapta as cores e transparência automaticamente para garantir contraste legível.
  - **Modo Matrix**: tema cyberpunk clássico com verde fosforescente.
- **Daemon em Segundo Plano**:
  - Monitora alterações de papel de parede no XFCE e atualiza o HUD em tempo real sem interrupções.

## Estrutura do Repositório

```text
├── autostart/
│   └── conky.desktop          # Entrada para inicialização automática no boot
├── config/
│   ├── colors.lua             # Tabela de cores carregada dinamicamente
│   ├── conky.conf             # Configuração principal do Conky
│   ├── restart_conky.sh       # Script de reinicialização rápida
│   ├── start_conky.sh         # Script de inicialização e disparo do daemon
│   ├── stop_conky.sh          # Script de finalização limpa
│   ├── theme_mode.txt         # Modo de tema ativo (matrix ou dynamic)
│   └── scripts/
│       ├── gpu_info.sh        # Leitor de frequência de GPU Intel DRM
│       ├── wallpaper_monitor.py # Daemon que vigia mudanças no papel de parede
│       └── wallpaper_theme.py   # Gerador de paletas adaptativas com PIL
├── install.sh                 # Script de instalação e configuração
├── uninstall.sh               # Script de desinstalação
└── README.md
```

## Instalação

Clone o repositório e execute o instalador:

```bash
git clone git@github.com:Pedro-Wilson/conky-system-monitor.git
cd conky-system-monitor
chmod +x install.sh
./install.sh
```

## Controle e Comandos Úteis

- **Alternar para Modo Matrix**:
  ```bash
  python3 ~/.config/conky/scripts/wallpaper_theme.py --matrix
  ```
- **Alternar para Modo Dinâmico (adapta ao papel de parede)**:
  ```bash
  python3 ~/.config/conky/scripts/wallpaper_theme.py --dynamic
  ```
- **Reiniciar o Conky**:
  ```bash
  ~/.config/conky/restart_conky.sh
  ```
- **Parar o Conky**:
  ```bash
  ~/.config/conky/stop_conky.sh
  ```
