#!/bin/bash
# proto_build_maum_only.sh

set -e

# .proto file path
INCLUDE_DIR="/home/jamong/manage_service/lib"
# pb2 file path
OUTPUT_DIR="/home/jamong/manage_service/lib"

echo "=== maum 패키지만 빌드 ==="
echo "소스: $INCLUDE_DIR"
echo "Python 출력: $OUTPUT_DIR"

# 출력 디렉토리 생성
mkdir -p "$OUTPUT_DIR"

# 1. maum 관련 proto 파일만 검색
echo "1. maum 관련 Proto 파일 검색..."
MAUM_PROTOS=$(find "$INCLUDE_DIR" -name "*.proto" -type f | grep -E "(maum|m2u)" | grep -v "google/protobuf")

if [ -z "$MAUM_PROTOS" ]; then
    echo "   maum 관련 파일이 없습니다. 다른 패턴으로 검색..."
    # google 파일 제외하고 모든 파일
    MAUM_PROTOS=$(find "$INCLUDE_DIR" -name "*.proto" -type f | grep -v "google/protobuf")
fi
PROTO_COUNT=$(echo "$MAUM_PROTOS" | wc -l)
echo "   발견된 proto 파일: $PROTO_COUNT 개"

# 첫 10개 파일 출력
echo "   파일 목록 (처음 10개):"
echo "$MAUM_PROTOS" | head -10 | sed 's/^/      /'

# 2. 기존 생성 파일들 정리
echo "2. 기존 생성 파일들 정리..."
find "$OUTPUT_DIR" -name "*_pb2*.py" -delete 2>/dev/null || true

# 3. grpcio-tools로 컴파일
echo "3. grpcio-tools로 컴파일..."
cd "$OUTPUT_DIR"

python -m grpc_tools.protoc \
       --proto_path="$INCLUDE_DIR" \
       --python_out="$OUTPUT_DIR" \
       --grpc_python_out="$OUTPUT_DIR" \
       $MAUM_PROTOS

# 4. __init__.py 파일들 생성
echo "4. __init__.py 파일들 생성..."
find "$OUTPUT_DIR" -type d -exec touch {}/__init__.py \; 2>/dev/null || true

# 5. 결과 확인
echo "5. 빌드 결과 확인..."
PB2_COUNT=$(find "$OUTPUT_DIR" -name "*_pb2.py" | wc -l)
GRPC_COUNT=$(find "$OUTPUT_DIR" -name "*_pb2_grpc.py" | wc -l)

echo "   생성된 pb2 파일: $PB2_COUNT 개"
echo "   생성된 grpc 파일: $GRPC_COUNT 개"

# 생성된 파일들 샘플 출력
if [ $PB2_COUNT -gt 0 ]; then
    echo "   생성된 pb2 파일들 (샘플):"
    find "$OUTPUT_DIR" -name "*_pb2.py" | head -5 | sed 's/^/      /'
fi

# 디렉토리 구조 출력
echo "6. 생성된 디렉토리 구조:"
find "$OUTPUT_DIR" -type d | grep -v "__pycache__" | head -10 | sort | sed 's/^/   /'

if [ $PB2_COUNT -gt 0 ]; then
    echo "=== 빌드 성공! ==="
else
    echo "=== 빌드 실패! ==="
    exit 1
fi
