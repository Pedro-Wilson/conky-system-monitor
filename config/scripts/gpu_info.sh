#!/usr/bin/env bash
# GPU Info Helper Script for Intel HD Graphics (ThinkPad L440 / Linux DRM)

card=$(ls -d /sys/class/drm/card[0-9] 2>/dev/null | head -n 1)

if [ -z "$card" ]; then
    echo "N/D"
    exit 0
fi

act_file="$card/gt_act_freq_mhz"
cur_file="$card/gt_cur_freq_mhz"
max_file="$card/gt_max_freq_mhz"

if [ -f "$act_file" ]; then
    act=$(cat "$act_file" 2>/dev/null)
elif [ -f "$cur_file" ]; then
    act=$(cat "$cur_file" 2>/dev/null)
else
    act=0
fi

[ -z "$act" ] && act=0

max=1250
if [ -f "$max_file" ]; then
    max=$(cat "$max_file" 2>/dev/null)
fi
[ -z "$max" ] && max=1250

pct=0
if [ "$max" -gt 0 ] 2>/dev/null; then
    pct=$(( act * 100 / max ))
fi

case "$1" in
    freq)
        echo "${act} MHz"
        ;;
    pct)
        echo "${pct}"
        ;;
    *)
        echo "${act} MHz (${pct}%)"
        ;;
esac
