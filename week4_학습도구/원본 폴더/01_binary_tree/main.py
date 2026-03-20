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
        self.status_label = ttk.Label(self.top_frame, text="순회 알고리즘을 선택하세요.", font=('Malgun Gothic', 12, 'bold'), foreground="#0056b3")
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

# --- 이진 트리 순회 구현 ---

class TreeNode:
    def __init__(self, value, x, y):
        self.value = value; self.x = x; self.y = y
        self.left = None; self.right = None; self.ui_id = None

TRAVERSAL_LOGIC = {
    "Preorder (전위)": {
        "code": """def preorder(node):
    if not node:
        return
    visit(node)
    preorder(node.left)
    preorder(node.right)""",
        "lines": [1, 2, 3, 4, 5]
    },
    "Inorder (중위)": {
        "code": """def inorder(node):
    if not node:
        return
    inorder(node.left)
    visit(node)
    inorder(node.right)""",
        "lines": [1, 2, 3, 4, 5]
    },
    "Postorder (후위)": {
        "code": """def postorder(node):
    if not node:
        return
    postorder(node.left)
    postorder(node.right)
    visit(node)""",
        "lines": [1, 2, 3, 4, 5, 6]
    }
}

def gen_preorder(node):
    yield 1, {"node": node.value if node else None, "action": "check"}
    if not node:
        yield 2, {"node": None, "action": "return"}
        return
    yield 3, {"node": node, "action": "visit"}
    yield 4, {"node": node, "action": "go_left"}
    yield from gen_preorder(node.left)
    yield 5, {"node": node, "action": "go_right"}
    yield from gen_preorder(node.right)

def gen_inorder(node):
    yield 1, {"node": node.value if node else None, "action": "check"}
    if not node:
        yield 2, {"node": None, "action": "return"}
        return
    yield 3, {"node": node, "action": "go_left"}
    yield from gen_inorder(node.left)
    yield 4, {"node": node, "action": "visit"}
    yield 5, {"node": node, "action": "go_right"}
    yield from gen_inorder(node.right)

def gen_postorder(node):
    yield 1, {"node": node.value if node else None, "action": "check"}
    if not node:
        yield 2, {"node": None, "action": "return"}
        return
    yield 3, {"node": node, "action": "go_left"}
    yield from gen_postorder(node.left)
    yield 4, {"node": node, "action": "go_right"}
    yield from gen_postorder(node.right)
    yield 5, {"node": node, "action": "visit"}

class BinaryTreeVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__("이진 트리 순회 시각화 (3-Way)")
        self.radius = 22
        self.traversal_result = []
        
        # 순회 모드 선택 UI 추가
        self.mode_label = ttk.Label(self.control_frame, text="순회 방식:")
        self.mode_label.pack(side=tk.LEFT, padx=(10, 2))
        self.mode_combo = ttk.Combobox(self.control_frame, values=list(TRAVERSAL_LOGIC.keys()), state="readonly", width=15)
        self.mode_combo.current(0)
        self.mode_combo.pack(side=tk.LEFT, padx=2)
        self.mode_combo.bind("<<ComboboxSelected>>", lambda e: self.reset())

        self.build_tree()
        self.on_reset()

    def build_tree(self):
        self.root_node = TreeNode(1, 350, 100)
        self.root_node.left = TreeNode(2, 175, 200)
        self.root_node.right = TreeNode(3, 525, 200)
        self.root_node.left.left = TreeNode(4, 90, 300)
        self.root_node.left.right = TreeNode(5, 260, 300)
        self.root_node.right.left = TreeNode(6, 440, 300)
        self.root_node.right.right = TreeNode(7, 610, 300)

    def draw_node(self, node):
        if not node: return
        if node.left:
            self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, width=2, fill="#bdc3c7")
            self.draw_node(node.left)
        if node.right:
            self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, width=2, fill="#bdc3c7")
            self.draw_node(node.right)
        
        r = self.radius
        node.ui_id = self.canvas.create_oval(node.x-r, node.y-r, node.x+r, node.y+r, fill='#ecf0f1', outline='#2c3e50', width=2)
        self.canvas.create_text(node.x, node.y, text=str(node.value), font=('Arial', 10, 'bold'))

    def draw_result(self, result):
        self.canvas.delete("result_ui")
        start_x = 50; start_y = 550; size = 40
        self.canvas.create_text(start_x, start_y-30, text="TRAVERSAL ORDER", font=('Consolas', 11, 'bold'), anchor=tk.W, tags="result_ui")
        for i, val in enumerate(result):
            x = start_x + i * (size+5)
            self.canvas.create_rectangle(x, start_y, x+size, start_y+size, fill="#2ecc71", outline="#27ae60", tags="result_ui")
            self.canvas.create_text(x+size/2, start_y+size/2, text=str(val), fill="white", font=('Arial', 10, 'bold'), tags="result_ui")

    def get_generator(self):
        mode = self.mode_combo.get()
        if "Preorder" in mode: return gen_preorder(self.root_node)
        if "Inorder" in mode: return gen_inorder(self.root_node)
        return gen_postorder(self.root_node)

    def on_step(self, ln, sd):
        action = sd.get("action"); node = sd.get("node")
        if isinstance(node, TreeNode):
            if action == "check": self.canvas.itemconfig(node.ui_id, fill="#f1c40f")
            elif action == "visit":
                self.canvas.itemconfig(node.ui_id, fill="#2ecc71")
                self.traversal_result.append(node.value)
                self.draw_result(self.traversal_result)
            elif action in ["go_left", "go_right"]: self.canvas.itemconfig(node.ui_id, fill="#3498db")

        self.update_state({
            "현재 노드": node.value if isinstance(node, TreeNode) else "None",
            "동작": action,
            "결과 리스트": str(self.traversal_result)
        })

    def on_reset(self): 
        self.traversal_result = []
        self.canvas.delete("all")
        self.draw_node(self.root_node)
        mode = self.mode_combo.get()
        self.set_code(TRAVERSAL_LOGIC[mode]["code"])
        self.draw_result([])
        self.status_label.config(text=f"{mode} 모드로 준비되었습니다.")

if __name__ == "__main__": BinaryTreeVisualizer().mainloop()
