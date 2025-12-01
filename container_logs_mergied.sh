#!/bin/bash

# 사용법 출력 함수
usage() {
    echo "Usage: $0 <container1> <container2> ... <containerN>"
    echo "Example: $0 nginx mysql redis"
    echo ""
    echo "Options:"
    echo "  -f, --follow    Follow log output (like tail -f)"
    echo "  -n, --lines N   Number of lines to show from each container (default: 100)"
    echo "  -h, --help      Show this help message"
    exit 1
}

# 기본값 설정
FOLLOW=false
LINES=100
CONTAINERS=()

# 인자 파싱
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        -n|--lines)
            LINES="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            CONTAINERS+=("$1")
            shift
            ;;
    esac
done

# 컨테이너가 지정되지 않은 경우
if [ ${#CONTAINERS[@]} -eq 0 ]; then
    echo "Error: No containers specified"
    usage
fi

# 컨테이너 존재 확인
for container in "${CONTAINERS[@]}"; do
    if ! docker ps -a --format '{{.Names}}' | grep -q "^${container}$"; then
        echo "Error: Container '${container}' not found"
        exit 1
    fi
done

# 임시 파일 생성
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Follow 모드
if [ "$FOLLOW" = true ]; then
    echo "Following logs from: ${CONTAINERS[*]} (last $LINES lines + new logs)"
    echo "Press Ctrl+C to stop"
    echo "----------------------------------------"

    # 각 컨테이너의 로그를 백그라운드에서 실행
    for container in "${CONTAINERS[@]}"; do
        docker logs -f --timestamps --tail "$LINES" "$container" 2>&1 | while read -r line; do
            echo "[$container] $line"
        done &
    done

    # 모든 백그라운드 프로세스 대기
    wait
else
    # 일회성 로그 출력
    echo "Fetching logs from: ${CONTAINERS[*]}"
    echo "----------------------------------------"

    # 각 컨테이너의 로그를 임시 파일에 저장
    for container in "${CONTAINERS[@]}"; do
        docker logs --timestamps --tail "$LINES" "$container" 2>&1 | \
            awk -v container="$container" '{print $0 " [" container "]"}' \
            >> "$TEMP_DIR/all_logs.txt"
    done

    # 시간순으로 정렬하여 출력
    if [ -f "$TEMP_DIR/all_logs.txt" ]; then
        sort "$TEMP_DIR/all_logs.txt"
    else
        echo "No logs found"
    fi
fi
