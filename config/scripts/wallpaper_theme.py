#!/usr/bin/env python3
"""
Dynamic Theme Generator for Conky (Sys Monitor)
Lenovo ThinkPad L440 - Zorin OS / XFCE
Supports:
  - MATRIX Green Theme (Cyberpunk / Terminal Phosphor Green)
  - DYNAMIC Wallpaper Contrast Theme (Adapts automatically to wallpaper changes)
"""

import sys
import os
import colorsys
import subprocess
import json
from PIL import Image

CONKY_DIR = os.path.expanduser("~/.config/conky")
COLORS_LUA = os.path.join(CONKY_DIR, "colors.lua")
MODE_FILE = os.path.join(CONKY_DIR, "theme_mode.txt")

def get_theme_mode():
    """Returns 'matrix' or 'dynamic'."""
    if os.path.isfile(MODE_FILE):
        try:
            with open(MODE_FILE, "r") as f:
                mode = f.read().strip().lower()
                if mode in ("matrix", "dynamic"):
                    return mode
        except Exception:
            pass
    return "matrix"

def set_theme_mode(mode):
    try:
        os.makedirs(CONKY_DIR, exist_ok=True)
        with open(MODE_FILE, "w") as f:
            f.write(mode.strip().lower() + "\n")
    except Exception as e:
        print(f"Error saving theme mode: {e}", file=sys.stderr)

def get_current_wallpaper():
    """Identifies the active wallpaper path from XFCE desktop settings."""
    monitors = []
    try:
        res = subprocess.run(['xrandr', '--query'], capture_output=True, text=True, timeout=2)
        for line in res.stdout.splitlines():
            if ' connected' in line:
                monitors.append(line.split()[0])
    except Exception:
        pass

    try:
        res = subprocess.run(['xfconf-query', '-c', 'xfce4-desktop', '-lv'], capture_output=True, text=True, timeout=2)
        lines = res.stdout.splitlines()
        candidates = {}
        for line in lines:
            parts = line.split(None, 1)
            if len(parts) == 2:
                prop, val = parts[0], parts[1].strip()
                if 'image' in prop and os.path.isfile(val):
                    candidates[prop] = val

        for mon in monitors:
            for prop, val in candidates.items():
                if mon in prop:
                    return val

        if candidates:
            return list(candidates.values())[0]
    except Exception:
        pass

    fallback_dir = os.path.expanduser("~/Imagens/wallpaper")
    if os.path.isdir(fallback_dir):
        for f in os.listdir(fallback_dir):
            full = os.path.join(fallback_dir, f)
            if os.path.isfile(full) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                return full

    return None

def compute_matrix_theme():
    """Generates the iconic Matrix Terminal phosphor green theme."""
    return {
        'mode': 'MATRIX',
        'own_window_colour': '020702',
        'own_window_argb_value': 220,
        'default_color': '00FF41',
        'color1': '00FF41',             -- Neon Phosphor Matrix Green (Primary HUD)
        'color2': 'E6FFE6',             -- Digital White-Green (High-voltage crisp numbers)
        'color3': '00CC44',             -- Phosphor Terminal Green (Labels)
        'color4': '003B14',             -- Cyber Matrix Grid Lines
        'color5': '39FF14',             -- Neon Cyber Mint Green (Secondary stats/graphs)
        'color6': 'FF3344',             -- Glitch Red Alert
        'down_graph_fade': '002B0E',
        'up_graph_fade': '00240B',
        'wallpaper': 'Matrix Terminal Protocol',
    }

def compute_dynamic_theme(image_path):
    """Generates a high-contrast palette adapted to the active wallpaper."""
    if not image_path or not os.path.isfile(image_path):
        return compute_matrix_theme()

    try:
        im = Image.open(image_path).convert('RGB')
    except Exception:
        return compute_matrix_theme()

    w, h = im.size
    crop_x = int(w * 0.65)
    crop_y = int(h * 0.65)
    top_right = im.crop((crop_x, 0, w, crop_y))
    tr_sample = top_right.resize((40, 40))
    tr_pixels = list(tr_sample.getdata())

    tr_lum = sum(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in tr_pixels) / (255.0 * len(tr_pixels))
    is_dark = tr_lum < 0.52

    sample_img = im.resize((100, 100), Image.Resampling.BOX)
    pixels = list(sample_img.getdata())

    bins = [0.0] * 24
    for r, g, b in pixels:
        h_norm, l_norm, s_norm = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        if s_norm > 0.12 and 0.08 < l_norm < 0.92:
            idx = int(h_norm * 24) % 24
            weight = s_norm * (1.0 - abs(l_norm - 0.5))
            bins[idx] += weight

    sorted_bins = sorted(range(24), key=lambda i: bins[i], reverse=True)
    total_vibrant = sum(bins)

    if total_vibrant < 10.0:
        h1 = 0.52
        h2 = 0.58
    else:
        best_bin = sorted_bins[0]
        h1 = best_bin / 24.0
        h2 = None
        for b_idx in sorted_bins[1:]:
            diff = abs(b_idx - best_bin)
            if diff > 12:
                diff = 24 - diff
            if diff >= 3 and bins[b_idx] > 0.12 * bins[best_bin]:
                h2 = b_idx / 24.0
                break
        if h2 is None:
            h2 = (h1 + 0.12) % 1.0

    def hls_to_hex(h, l, s):
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f'{int(round(r * 255)):02X}{int(round(g * 255)):02X}{int(round(b * 255)):02X}'

    if is_dark:
        bg_col = '0A0E14'
        bg_alpha = 205
        color1 = hls_to_hex(h1, 0.64, 0.96)
        color2 = 'FFFFFF'
        color3 = 'B0BAC5'
        color4 = '252D3A'
        color5 = hls_to_hex(h2, 0.68, 0.90)
        color6 = 'FBBF24'
        down_fade = hls_to_hex(h1, 0.12, 0.85)
        up_fade = hls_to_hex(h2, 0.12, 0.85)
    else:
        bg_col = 'FFFFFF'
        bg_alpha = 220
        color1 = hls_to_hex(h1, 0.35, 0.96)
        color2 = '0F172A'
        color3 = '475569'
        color4 = 'CBD5E1'
        color5 = hls_to_hex(h2, 0.38, 0.90)
        color6 = 'D97706'
        down_fade = 'E2E8F0'
        up_fade = 'E2E8F0'

    return {
        'mode': 'DARK' if is_dark else 'LIGHT',
        'own_window_colour': bg_col,
        'own_window_argb_value': bg_alpha,
        'default_color': color2,
        'color1': color1,
        'color2': color2,
        'color3': color3,
        'color4': color4,
        'color5': color5,
        'color6': color6,
        'down_graph_fade': down_fade,
        'up_graph_fade': up_fade,
        'wallpaper': image_path,
    }

def compute_theme(image_path=None):
    mode = get_theme_mode()
    if mode == 'matrix':
        return compute_matrix_theme()
    return compute_dynamic_theme(image_path)

def write_colors_lua(theme):
    """Outputs the Lua table loaded by conky.conf."""
    lua_code = f"""-- Auto-generated by wallpaper_theme.py
-- Theme Mode: {theme['mode']}
-- Source: {theme.get('wallpaper', 'default')}

return {{
    own_window_colour = '{theme['own_window_colour']}',
    own_window_argb_value = {theme['own_window_argb_value']},
    default_color = '#{theme['default_color']}',
    color1 = '{theme['color1']}',
    color2 = '{theme['color2']}',
    color3 = '{theme['color3']}',
    color4 = '{theme['color4']}',
    color5 = '{theme['color5']}',
    color6 = '{theme['color6']}',
    down_graph_fade = '{theme['down_graph_fade']}',
    up_graph_fade = '{theme['up_graph_fade']}',
}}
"""
    os.makedirs(CONKY_DIR, exist_ok=True)
    temp_file = COLORS_LUA + ".tmp"
    with open(temp_file, "w") as f:
        f.write(lua_code)
    os.replace(temp_file, COLORS_LUA)

def reload_conky():
    """Signals running conky with SIGUSR1 to reload configuration live."""
    try:
        user = os.environ.get('USER') or os.path.basename(os.path.expanduser("~"))
        pids = subprocess.run(['pgrep', '-u', user, '-x', 'conky'],
                              capture_output=True, text=True).stdout.strip().split()
        if pids:
            for pid in pids:
                try:
                    os.kill(int(pid), 10)  # 10 is SIGUSR1
                except Exception:
                    pass
            return True
    except Exception as e:
        print(f"Error reloading conky: {e}", file=sys.stderr)
    return False

def apply(wallpaper_path=None):
    wp = wallpaper_path or get_current_wallpaper()
    theme = compute_theme(wp)
    write_colors_lua(theme)
    reload_conky()
    return theme

if __name__ == '__main__':
    target_wp = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == '--matrix':
            set_theme_mode('matrix')
            t = apply()
            print(f"Theme set to MATRIX Green (Phosphor HUD)!")
            sys.exit(0)
        elif arg == '--dynamic':
            set_theme_mode('dynamic')
            t = apply()
            print(f"Theme set to DYNAMIC Wallpaper Contrast!")
            sys.exit(0)
        elif arg == '--print':
            wp = get_current_wallpaper()
            print(json.dumps(compute_theme(wp), indent=2))
            sys.exit(0)
        elif arg == '--apply':
            pass
        elif os.path.isfile(sys.argv[1]):
            target_wp = sys.argv[1]

    t = apply(target_wp)
    print(f"Applied {t['mode']} theme: color1=#{t['color1']}, bg=#{t['own_window_colour']}")
