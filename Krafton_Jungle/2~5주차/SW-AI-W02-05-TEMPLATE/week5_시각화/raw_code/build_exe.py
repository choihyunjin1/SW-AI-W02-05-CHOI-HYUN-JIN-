import os
import subprocess
import shutil
import sys

def build_exes():
    base_dir = r"C:\Users\cedis\OneDrive\문서\ANTIWORK\Krafton_Jungle\2~5주차\SW-AI-W02-05-TEMPLATE\week5_시각화"
    raw_code_dir = os.path.join(base_dir, "raw_code")
    dist_dir = os.path.join(base_dir, "win배포용")
    
    # 윈도우 한글 인코딩 문제 방지를 위해 CWD 변경
    os.chdir(raw_code_dir)
    
    files_to_build = [
        "01_dp_fibonacci_vis.py",
        "02_dp_stairs_vis.py",
        "03_greedy_coin_vis.py",
        "04_greedy_meeting_vis.py"
    ]
    
    print(f"[{'PyInstaller 빌드 시작':^20}]")
    for py_file in files_to_build:
        print(f"[{py_file}] 빌드 중...")
        # PyInstaller 기본 명령어 (콘솔숨김: --noconsole, 단일파일: --onefile)
        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--onefile",
            "--windowed", # 콘솔창 X
            py_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f" -> 성공!")
            exe_name = py_file.replace(".py", ".exe")
            src_exe = os.path.join(raw_code_dir, "dist", exe_name)
            dst_exe = os.path.join(dist_dir, exe_name)
            
            # 빌드된 exe 파일을 배포용 폴더로 이동
            if os.path.exists(src_exe):
                shutil.copy2(src_exe, dst_exe)
                print(f" -> {dst_exe} 복사 완료")
            else:
                print(f" -> 경고: EXE 파일이 {src_exe}에 없습니다.")
        else:
            print(f" -> 실패! 에러 로그:")
            print(result.stderr)
            
    print("\n[{'빌드 프로세스 종료':^20}]")
    print("원하는 경우 raw_code/build 및 dist 폴더를 삭제할 수 있습니다.")

if __name__ == "__main__":
    build_exes()
