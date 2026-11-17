#!/usr/bin/env python3
"""
Background Wallpaper Monitor Daemon for Conky
Lenovo ThinkPad L440 - Zorin OS / XFCE
Watches for wallpaper changes and automatically adapts Conky colors in real-time.
"""

import os
import sys
import time
import signal
import subprocess
import threading

# Add scripts directory to path to import wallpaper_theme
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import wallpaper_theme

PID_FILE = os.path.expanduser("~/.config/conky/.wallpaper_monitor.pid")
RUNNING = True

def signal_handler(signum, frame):
    global RUNNING
    RUNNING = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def check_single_instance():
    """Ensures only one instance of the monitor daemon runs."""
    if os.path.isfile(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            # Check if running
            os.kill(old_pid, 0)
            # If still running, kill it cleanly so the new one takes over
            os.kill(old_pid, signal.SIGTERM)
            time.sleep(0.3)
        except (ProcessLookupError, ValueError):
            pass
        except PermissionError:
            pass

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

def main():
    global RUNNING
    check_single_instance()

    last_wallpaper = None
    last_mtime = 0
    lock = threading.Lock()

    def update_if_changed(force=False):
        nonlocal last_wallpaper, last_mtime
        with lock:
            current_wp = wallpaper_theme.get_current_wallpaper()
            if not current_wp or not os.path.isfile(current_wp):
                return

            try:
                mtime = os.path.getmtime(current_wp)
            except Exception:
                mtime = 0

            if force or current_wp != last_wallpaper or mtime != last_mtime:
                last_wallpaper = current_wp
                last_mtime = mtime
                try:
                    theme = wallpaper_theme.apply(current_wp)
                    print(f"[wallpaper_monitor] Theme updated: {theme['mode']} (color1=#{theme['color1']}) from {current_wp}", flush=True)
                except Exception as e:
                    print(f"[wallpaper_monitor] Error applying theme: {e}", file=sys.stderr, flush=True)

    # Initial apply on launch
    update_if_changed(force=True)

    # Listener thread for xfconf-query events
    def xfconf_listener():
        while RUNNING:
            try:
                proc = subprocess.Popen(
                    ['xfconf-query', '-c', 'xfce4-desktop', '-m'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    bufsize=1
                )
                for line in proc.stdout:
                    if not RUNNING:
                        break
                    # If property change relates to wallpaper image
                    if any(key in line for key in ('last-image', 'image-path', 'workspace')):
                        time.sleep(0.2)  # Short debounce
                        update_if_changed()
                proc.terminate()
            except Exception as e:
                time.sleep(2)

    listener_thread = threading.Thread(target=xfconf_listener, daemon=True)
    listener_thread.start()

    # Periodic heartbeat / fallback poll every 4 seconds
    user = os.environ.get('USER') or os.path.basename(os.path.expanduser("~"))
    while RUNNING:
        try:
            time.sleep(4)
            if not RUNNING:
                break
            update_if_changed()

            # Ensure Conky is running if the monitor is active
            pids = subprocess.run(
                ['pgrep', '-u', user, '-x', 'conky'],
                capture_output=True, text=True
            ).stdout.strip()
            if not pids:
                start_script = os.path.expanduser("~/.config/conky/start_conky.sh")
                if os.path.isfile(start_script):
                    subprocess.Popen([start_script, "0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except KeyboardInterrupt:
            break

    if os.path.isfile(PID_FILE):
        try:
            os.remove(PID_FILE)
        except Exception:
            pass

if __name__ == '__main__':
    main()
