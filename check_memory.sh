#!/usr/bin/sh

watch -n 1 \
        'ps auxww --sort=-%mem | awk '\
        \' 'NR==1{printf "%-10s %-10s %-10s %-10s %-10s %-10s %s\n", $1, $2, $3, $4, "RSS(GB)", $8, $11; next}'\
        ' {printf "%-10s %-10s %-10s %-10s %-10.2f %-10s %s\n", $1, $2, $3, $4, $6/(1024*1024), $8, $11}'\'' | head -n 40'