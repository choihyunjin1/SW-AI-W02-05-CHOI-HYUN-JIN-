import tkinter as tk
from tkinter import ttk, font
import time

# --- 공통 UI 프레임워크 (내재화) ---

class BaseVisualizer(tk.Tk):
    def __init__(self, title="알고리즘 시각화", width=1200, height=750):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.setup_ui()
        self.generator = None
        self.is_playing = False
        self.delay = 800
        
    def setup_ui(self):
        self.top_frame = ttk.Frame(self, padding=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        self.status_label = ttk.Label(self.top_frame, text="알고리즘을 준비하고 시작하세요.", font=('Malgun Gothic', 12, 'bold'), foreground="#0056b3")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.control_frame = ttk.LabelFrame(self.top_frame, text="실행 제어", padding=5)
        self.control_frame.pack(side=tk.RIGHT, padx=10)
        self.btn_play = ttk.Button(self.control_frame, text="▶ Play", command=self.play)
        self.btn_play.pack(side=tk.LEFT, padx=3)
        self.btn_step = ttk.Button(self.control_frame, text="⏭ Step", command=self.step)
        self.btn_step.pack(side=tk.LEFT, padx=3)
        self.btn_reset = ttk.Button(self.control_frame, text="🔄 Reset", command=self.reset)
        self.btn_reset.pack(side=tk.LEFT, padx=3)

        self.speed_scale = ttk.Scale(self.control_frame, from_=2000, to=100, orient=tk.HORIZONTAL, command=self.update_speed)
        self.speed_scale.set(800)
        self.speed_scale.pack(side=tk.LEFT, padx=5)

        self.main_container = ttk.Frame(self, padding=5)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        self.viz_frame = ttk.LabelFrame(self.main_container, text="시각화 영역", padding=5)
        self.viz_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.viz_frame, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.info_frame = ttk.Frame(self.main_container, width=400)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        self.code_frame = ttk.LabelFrame(self.info_frame, text="Python Code", padding=5)
        self.code_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.code_text = tk.Text(self.code_frame, width=45, font=("Consolas", 11), bg="#1e1e1e", fg="#d4d4d4", padx=10, pady=10)
        self.code_text.pack(fill=tk.BOTH, expand=True)
        self.code_text.tag_configure("highlight", background="#3e3e3e")
        
        self.state_frame = ttk.LabelFrame(self.info_frame, text="변수 상태", padding=5)
        self.state_frame.pack(fill=tk.X)
        self.state_text = tk.Text(self.state_frame, height=8, width=45, font=("Consolas", 11), bg="#252526", fg="#cccccc")
        self.state_text.pack(fill=tk.X)

    def set_code(self, code):
        self.code_text.config(state=tk.NORMAL)
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, code.strip())
        self.code_text.config(state=tk.DISABLED)

    def highlight_line(self, line_num):
        self.code_text.config(state=tk.NORMAL)
        self.code_text.tag_remove("highlight", "1.0", tk.END)
        if line_num > 0:
            self.code_text.tag_add("highlight", f"{line_num}.0", f"{line_num}.end")
        self.code_text.config(state=tk.DISABLED)

    def update_state(self, state_dict):
        self.state_text.config(state=tk.NORMAL)
        self.state_text.delete(1.0, tk.END)
        for k, v in state_dict.items(): self.state_text.insert(tk.END, f"{k}: {v}\n")
        self.state_text.config(state=tk.DISABLED)

    def update_speed(self, val): self.delay = int(float(val))
    def play(self):
        if not self.is_playing:
            self.is_playing = True
            self.run_animation()
    def pause(self): self.is_playing = False
    def step(self): self.pause(); self._do_step()
    def reset(self):
        self.pause(); self.generator = None; self.canvas.delete("all")
        self.code_text.config(state=tk.NORMAL); self.code_text.tag_remove("highlight", "1.0", tk.END)
        self.status_label.config(text="초기화되었습니다."); self.on_reset()

    def _do_step(self):
        if not self.generator: self.generator = self.get_generator()
        try:
            ln, sd = next(self.generator)
            self.highlight_line(ln)
            if sd: self.update_state(sd)
            self.on_step(ln, sd)
            return True
        except StopIteration: return False

    def run_animation(self):
        if self.is_playing:
            if self._do_step(): self.after(self.delay, self.run_animation)
            else: self.is_playing = False

    def get_generator(self): raise NotImplementedError()
    def on_step(self, ln, sd): pass
    def on_reset(self): pass

# --- BFS 구현 ---

BFS_CODE = """def bfs_traversal(graph, start):
    visited = {start}
    queue = [start]
    while queue:
        curr = queue.pop(0)
        for neighbor in graph[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)"""

def gen_bfs_traversal(graph, start):
    visited = {start}; queue = [start]
    yield 4, {"queue": list(queue), "visited": list(visited)}
    while queue:
        curr = queue.pop(0)
        yield 6, {"curr": curr, "queue": list(queue), "visited": list(visited)}
        for neighbor in graph[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                yield 10, {"curr": curr, "neighbor": neighbor, "queue": list(queue)}

class BFSVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__("너비 우선 탐색 시각화")
        self.nodes = {1:(150,150), 2:(300,50), 3:(450,150), 4:(150,300), 5:(300,300), 6:(450,300)}
        self.edges = [(1,2), (1,4), (2,3), (2,5), (3,6), (4,5)]
        self.graph = {i:[] for i in self.nodes}
        for u,v in self.edges: self.graph[u].append(v); self.graph[v].append(u)
        self.on_reset()

    def draw_graph(self):
        for u,v in self.edges: self.canvas.create_line(self.nodes[u][0], self.nodes[u][1], self.nodes[v][0], self.nodes[v][1], fill="#bdc3c7", width=2)
        for k,(x,y) in self.nodes.items():
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="#ecf0f1", outline="#2c3e50", width=2, tags=f"node_{k}")
            self.canvas.create_text(x,y,text=str(k), font=('Arial', 10, 'bold'))

    def draw_queue(self, queue):
        """큐의 물리적 표현을 캔버스 하단에 그립니다."""
        self.canvas.delete("queue_ui")
        start_x = 50
        start_y = 450
        size = 40
        self.canvas.create_text(start_x, start_y-30, text="QUEUE (FIFO)", font=('Consolas', 11, 'bold'), anchor=tk.W, tags="queue_ui")
        # 큐 외곽선
        self.canvas.create_rectangle(start_x, start_y, start_x + 300, start_y + size, outline="#95a5a6", dash=(4,4), tags="queue_ui")
        
        for i, val in enumerate(queue):
            x = start_x + i * (size+5)
            self.canvas.create_rectangle(x, start_y, x+size, start_y+size, fill="#f39c12", outline="#e67e22", tags="queue_ui")
            self.canvas.create_text(x+size/2, start_y+size/2, text=str(val), fill="white", font=('Arial', 10, 'bold'), tags="queue_ui")

    def get_generator(self): return gen_bfs_traversal(self.graph, 1)
    
    def on_step(self, ln, sd):
        self.canvas.delete("highlight")
        curr = sd.get("curr"); visited = sd.get("visited", []); queue = sd.get("queue", [])
        neighbor = sd.get("neighbor")

        self.draw_queue(queue)
        
        for k in self.nodes:
            if k == curr: color = "#e74c3c" # 현재 노드
            elif k in visited: color = "#2ecc71" # 방문 완료
            else: color = "#ecf0f1"
            self.canvas.itemconfig(f"node_{k}", fill=color)

        if neighbor:
            nx, ny = self.nodes[neighbor]
            self.canvas.create_oval(nx-25, ny-25, nx+25, ny+25, outline="#f1c40f", width=3, tags="highlight")
            self.canvas.create_text(nx, ny-35, text="CHECK", fill="#f39c12", font=('Arial', 9, 'bold'), tags="highlight")

    def on_reset(self): 
        self.set_code(BFS_CODE)
        self.draw_graph()
        self.draw_queue([])

if __name__ == "__main__": BFSVisualizer().mainloop()
