import os
import subprocess

base_dir = r"C:\Users\cedis\OneDrive\문서\ANTIWORK\Krafton_Jungle\week4_학습도구\원본 폴더"
dist_dir = r"C:\Users\cedis\OneDrive\문서\ANTIWORK\Krafton_Jungle\week4_학습도구\.exe 배포판"

projects = {
    "01_binary_tree": "01_binary_tree",
    "02_bst": "02_bst",
    "03_graph_basic": "03_graph_basic",
    "04_bfs": "04_bfs",
    "05_dfs": "05_dfs",
    "06_topological_sort": "06_topological_sort"
}

python_exe = r"C:\Users\cedis\OneDrive\문서\ANTIWORK\.venv\Scripts\python.exe"

# 개별 도구 빌드 (이제 각각 단일 파일로 구성됨)
for folder, name in projects.items():
    working_dir = os.path.join(base_dir, folder)
    print(f"Building {name}...")
    cmd = [
        python_exe, "-m", "PyInstaller",
        "-F", "--windowed",
        f"--distpath={dist_dir}",
        f"--name={name}",
        "main.py"
    ]
    subprocess.run(cmd, cwd=working_dir)

print("All builds completed!")
