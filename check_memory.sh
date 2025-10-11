#!/usr/bin/env sh

# 메모리 사용량 모니터링 - 내림차순 (Ctrl+C로 종료)
if [[ "$OSTYPE" == "darwin"* ]]; then
    while true; do
        clear
        ps auxww | sort -k4 -rn | head -n 21 | awk '
        NR==1{
            printf "%-10s %-10s %-10s %-10s %-10s %-10s %s\n", "USER", "PID", "%CPU", "%MEM", "RSS(GB)", "STAT", "COMMAND"
            next
        }
        {
            printf "%-10s %-10s %-10s %-10s %-10.2f %-10s %s\n", $1, $2, $3, $4, $6/(1024*1024), $8, $11
        }'
        sleep 1
    done
else
    watch -n 1 'ps auxww --sort=-%mem | awk '\''
    NR==1{
        printf "%-10s %-10s %-10s %-10s %-10s %-10s %s\n", $1, $2, $3, $4, "RSS(GB)", $8, $11
        next
    }
    NR<=40{
        printf "%-10s %-10s %-10s %-10s %-10.2f %-10s %s\n", $1, $2, $3, $4, $6/(1024*1024), $8, $11
    }'\''
    '
fi
