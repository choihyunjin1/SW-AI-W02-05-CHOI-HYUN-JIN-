import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

class AlgoLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AlgoViz - 알고리즘 학습 도구")
        self.geometry("600x500")
        self.configure(bg="#1e1e1e")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Determine the base path for algorithms
        if getattr(sys, 'frozen', False):
            # If bundled by PyInstaller
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self, bg="#2d2d2d", height=80)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Algorithm Visualization", font=("Arial", 20, "bold"), fg="#58a6ff", bg="#2d2d2d").pack(pady=20)

        # Main Grid
        grid_frame = tk.Frame(self, bg="#1e1e1e", padx=20, pady=20)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        algorithms = [
            ("이진 트리 순회", "01_binary_tree", "🌳"),
            ("BST 검색", "02_bst", "🔍"),
            ("그래프 기본 탐색", "03_graph_basic", "🕸️"),
            ("너비 우선 탐색 (BFS)", "04_bfs", "🌊"),
            ("깊이 우선 탐색 (DFS)", "05_dfs", "🔦"),
            ("위상 정렬 (Topo Sort)", "06_topological_sort", "📐")
        ]

        for i, (name, folder, icon) in enumerate(algorithms):
            row, col = i // 2, i % 2
            btn = tk.Button(grid_frame, text=f"{icon} {name}", font=("Arial", 12), 
                           command=lambda f=folder: self.run_algo(f),
                           bg="#333333", fg="white", activebackground="#444444", 
                           activeforeground="#58a6ff", height=3, width=25, relief=tk.FLAT)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for i in range(2): grid_frame.columnconfigure(i, weight=1)
        for i in range(3): grid_frame.rowconfigure(i, weight=1)

        # Footer
        footer = tk.Label(self, text="© 2026 Antigravity Algorithm Suite", font=("Arial", 9), fg="#888888", bg="#1e1e1e")
        footer.pack(side=tk.BOTTOM, pady=10)

    def run_algo(self, folder_name):
        # Construct the path to the original main.py
        script_path = os.path.join(self.base_path, "원본 폴더", folder_name, "main.py")
        
        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"Could not find script at:\n{script_path}")
            return

        try:
            # Run the script in a separate process
            subprocess.Popen([sys.executable, script_path])
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

if __name__ == "__main__":
    app = AlgoLauncher()
    app.mainloop()
