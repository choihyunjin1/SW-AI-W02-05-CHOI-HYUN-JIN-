#!/bin/bash

echo "🚀 개별 알고리즘 맥 앱 최종 빌드 프로세스 시작 (한글 명칭 직접 적용)..."

# 1. '맥 배포용' 및 '윈도우 배포용' 폴더 정리 (기존 항목 삭제 후 재생성)
rm -rf "/Users/choehyeonjin/.gemini/antigravity/scratch/00_맥_최종_배포용"
rm -rf "/Users/choehyeonjin/.gemini/antigravity/scratch/00_윈도우_최종_배포용"
mkdir -p "/Users/choehyeonjin/.gemini/antigravity/scratch/00_맥_최종_배포용"
mkdir -p "/Users/choehyeonjin/.gemini/antigravity/scratch/00_윈도우_최종_배포용"

# 2. 윈도우용 분류 가이드
printf "여기에 사용자께서 윈도우에서 직접 제작하신 .exe 파일들을 넣어주세요.\n현재 폴더 분류를 위해 미리 생성해 두었습니다." > "/Users/choehyeonjin/.gemini/antigravity/scratch/00_윈도우_최종_배포용/여기에_EXE를_넣어주세요.txt"

# 3. 개별 빌드 함수
build_final() {
    local dir=$1
    local name=$2
    local script="/Users/choehyeonjin/.gemini/antigravity/scratch/week4_학습도구/원본 폴더/$dir/main.py"
    
    echo "📦 [$name] 맥 앱 빌드 중..."
    # 한글 이름을 직접 name으로 지정하여 Info.plist 정합성 확보
    pyinstaller --name "$name" --windowed --noconfirm --clean "$script"
    
    if [ -d "dist/$name.app" ]; then
        # 1. .app를 '00_맥_최종_배포용'으로 이동
        mv "dist/$name.app" "/Users/choehyeonjin/.gemini/antigravity/scratch/00_맥_최종_배포용/"
        
        # 2. 보안 격리 해제 및 권한 부여 (필수)
        local target="/Users/choehyeonjin/.gemini/antigravity/scratch/00_맥_최종_배포용/$name.app"
        chmod +x "$target/Contents/MacOS/$name"
        xattr -cr "$target"
        
        # 3. 100% 실행 보장용 .command 파일 생성
        local cmd_file="/Users/choehyeonjin/.gemini/antigravity/scratch/00_맥_최종_배포용/${name}_직접실행.command"
        cat <<EOF > "$cmd_file"
#!/bin/bash
cd "\$(dirname "\$0")"
echo "[$name] 실행 중..."
python3 "$script"
EOF
        chmod +x "$cmd_file"
        
        echo "✅ [$name] 배포 준비 완료!"
    fi
    # 중간 부산물 제거
    rm -rf build dist *.spec
}

# 4. 6개 알고리즘 순차적 빌드
cd "/Users/choehyeonjin/.gemini/antigravity/scratch/week4_학습도구/"
build_final "01_binary_tree" "01_너비우선탐색_맥북전용"
build_final "02_bst" "02_BST검색_맥북전용"
build_final "03_graph_basic" "03_그래프기본_맥북전용"
build_final "04_bfs" "04_BFS탐색_맥북전용"
build_final "05_dfs" "05_DFS탐색_맥북전용"
build_final "06_topological_sort" "06_위상정렬_맥북전용"

echo "✨ 모든 작업이 완료되었습니다! '/Users/choehyeonjin/.gemini/antigravity/scratch/00_맥_최종_배포용' 폴더를 확인하세요."
ls -F "/Users/choehyeonjin/.gemini/antigravity/scratch/00_맥_최종_배포용"
