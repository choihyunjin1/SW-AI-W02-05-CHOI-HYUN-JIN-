import os
import subprocess

base_dir = r"C:\Users\cedis\OneDrive\문서\ANTIWORK\week3_학습도구\원본 파일"
dist_dir = r"C:\Users\cedis\OneDrive\문서\ANTIWORK\week3_학습도구\window_배포용"
python_exe = r"C:\Users\cedis\AppData\Local\Microsoft\WindowsApps\python.exe"

targets = [
    ("01_binary_search", "01_이분탐색_학습도구"),
    ("02_divide_conquer", "02_분할정복_학습도구"),
    ("03_quick_sort", "03_퀵정렬_학습도구"),
    ("04_merge_sort", "04_병합정렬_학습도구"),
    ("05_stack", "05_스택_학습도구"),
    ("06_queue", "06_큐_학습도구"),
    ("07_priority_queue", "07_우선순위큐_학습도구"),
    ("08_linked_list", "08_연결리스트_학습도구"),
    ("09_hash_table", "09_해시테이블_학습도구")
]

print("순차 빌드를 시작합니다. (PyInstaller)")
for folder, name in targets:
    # 이미 생성된 exe가 있으면 스킵
    exe_path = os.path.join(dist_dir, f"{name}.exe")
    if os.path.exists(exe_path):
        print(f"[{name}] 이미 빌드되어 있습니다. 스킵합니다.")
        continue

    print(f"[{name}] 빌드 시작...")
    cwd = os.path.join(base_dir, folder)
    cmd = [
        python_exe, "-m", "PyInstaller",
        "--noconfirm", "--onefile", "--windowed",
        "--name", name,
        "--distpath", dist_dir,
        "main.py"
    ]
    try:
        subprocess.run(cmd, cwd=cwd, check=True, capture_output=True)
        print(f"[{name}] 빌드 성공!")
    except subprocess.CalledProcessError as e:
        print(f"[{name}] 빌드 실패!")
        print(e.stderr.decode("utf-8", errors="ignore"))
    print("-" * 40)
print("모든 빌드 작업 완료!")
