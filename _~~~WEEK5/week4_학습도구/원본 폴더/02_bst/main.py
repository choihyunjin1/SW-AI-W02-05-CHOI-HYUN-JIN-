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

# --- BST Search 구현 ---

BST_CODE = """def bst_search(node, target):
    curr = node
    while curr:
        if curr.val == target:
            return curr
        if target < curr.val:
            curr = curr.left
        else:
            curr = curr.right
    return None"""

def gen_bst_search(node, target):
    curr = node
    yield 2, {"curr": curr['val'] if curr else "None", "action": "init"}
    while curr:
        yield 3, {"curr": curr['val'], "action": "check_while"}
        yield 4, {"curr": curr['val'], "action": "check_target"}
        if curr['val'] == target:
            yield 5, {"curr": curr['val'], "action": "found"}
            return curr
        yield 6, {"curr": curr['val'], "action": "check_left"}
        if target < curr['val']:
            curr = curr['left']
            yield 7, {"curr": curr['val'] if curr else "None", "action": "go_left"}
        else:
            yield 8, {"curr": curr['val'], "action": "go_right"}
            curr = curr['right']
            yield 9, {"curr": curr['val'] if curr else "None", "action": "moved_right"}
    yield 10, {"curr": "None", "action": "not_found"}

class BSTVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__("이진 탐색 트리 검색 시각화")
        self.target = 45 # 시각적으로 찾을 타겟
        self.nodes_data = {
            1: {'val': 50, 'left': 2, 'right': 3, 'x': 300, 'y': 100},
            2: {'val': 30, 'left': 4, 'right': 5, 'x': 150, 'y': 200},
            3: {'val': 70, 'left': 6, 'right': 7, 'x': 450, 'y': 200},
            4: {'val': 20, 'left': 8, 'right': 9, 'x': 75, 'y': 300},
            5: {'val': 40, 'left': 10, 'right': 11, 'x': 225, 'y': 300},
            6: {'val': 60, 'left': 12, 'right': None, 'x': 375, 'y': 300},
            7: {'val': 80, 'left': None, 'right': None, 'x': 525, 'y': 300},
            8: {'val': 10, 'left': None, 'right': None, 'x': 35, 'y': 400},
            9: {'val': 25, 'left': None, 'right': None, 'x': 110, 'y': 400},
            10: {'val': 35, 'left': None, 'right': None, 'x': 185, 'y': 400},
            11: {'val': 45, 'left': None, 'right': None, 'x': 260, 'y': 400},
            12: {'val': 55, 'left': None, 'right': None, 'x': 340, 'y': 400}
        }
        for v in self.nodes_data.values():
            if v['left']: v['left'] = self.nodes_data[v['left']]
            if v['right']: v['right'] = self.nodes_data[v['right']]
        self.on_reset()

    def draw_tree(self):
        # 타겟 표시 전용 영역 그리기
        self.canvas.create_rectangle(20, 20, 180, 70, fill="#f8f9fa", outline="#dee2e6", width=2)
        self.canvas.create_text(100, 45, text=f"찾을 값: {self.target}", font=('Malgun Gothic', 12, 'bold'), fill="#dc3545")

        for v in self.nodes_data.values():
            if v['left']: self.canvas.create_line(v['x'], v['y'], v['left']['x'], v['left']['y'], fill="#bdc3c7", width=2)
            if v['right']: self.canvas.create_line(v['x'], v['y'], v['right']['x'], v['right']['y'], fill="#bdc3c7", width=2)
        for v in self.nodes_data.values():
            r = 22
            v['ui_id'] = self.canvas.create_oval(v['x']-r, v['y']-r, v['x']+r, v['y']+r, fill="#ecf0f1", outline="#2c3e50", width=2)
            self.canvas.create_text(v['x'], v['y'], text=str(v['val']), font=('Arial', 10, 'bold'))

    def get_generator(self): return gen_bst_search(self.nodes_data[1], self.target)
    
    def on_step(self, ln, sd):
        self.canvas.delete("highlight")
        curr_val = sd.get("curr")
        action = sd.get("action")
        
        for v in self.nodes_data.values():
            if v['val'] == curr_val:
                r = 28
                color = "green" if action == "found" else "red"
                self.canvas.create_oval(v['x']-r, v['y']-r, v['x']+r, v['y']+r, outline=color, width=4, tags="highlight")
                if action == "found":
                    self.canvas.create_text(v['x'], v['y']-45, text="FOUND!", font=('Impact', 16), fill="green", tags="highlight")
                elif action == "init":
                    self.canvas.create_text(v['x'], v['y']-45, text="START HERE", font=('Arial', 10, 'bold'), fill="red", tags="highlight")

    def on_reset(self): 
        self.set_code(BST_CODE)
        self.draw_tree()
        self.status_label.config(text=f"타겟 {self.target}을(를) 검색할 준비가 되었습니다.")

if __name__ == "__main__":
    BSTVisualizer().mainloop()
