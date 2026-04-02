import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import math

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.text = ""

    def showtip(self, text, x, y):
        if self.tipwindow and self.text == text: return
        if self.tipwindow: self.hidetip()
            
        self.text = text
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(1)
        self.tipwindow.wm_geometry(f"+{x + 15}+{y + 15}")
        
        label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("맑은 고딕", 10), padx=5, pady=3)
        label.pack()

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class DivideConquerVisualizer(tk.Tk):
    def __init__(self, arr, generator, delay=800):
        super().__init__()
        self.title("분할 정복 (Divide & Conquer) 시각화 학습 도구")
        self.arr = arr
        self.n = len(arr)
        self.generator = generator
        self.delay = delay 
        
        self.is_paused = True   
        self.is_finished = False 
        
        # 메인 프레임 구성
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.left_col = tk.Frame(self.top_frame)
        self.left_col.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.right_col = tk.Frame(self.top_frame)
        self.right_col.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        
        # ===== [좌측 영역: 분할 정복 재귀 트리 캔버스] =====
        self.canvas_width = 850
        self.canvas_height = 550
        self.canvas = tk.Canvas(self.left_col, width=self.canvas_width, height=self.canvas_height, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.canvas.pack(pady=5)
        
        self.status_var = tk.StringVar(value="초기화 중...")
        tk.Label(self.left_col, textvariable=self.status_var, font=("맑은 고딕", 12, "bold"), fg="blue").pack(pady=5)

        # 원본 배열 뷰용 프레임
        self.var_frame = tk.LabelFrame(self.left_col, text="💡 현재 탐색 대상(원본 배열)", font=("맑은 고딕", 11, "bold"), fg="#D32F2F")
        self.var_frame.pack(fill=tk.X, pady=5, ipadx=5, ipady=5)
        
        self.lbl_arr = tk.Label(self.var_frame, text=f"arr = {self.arr}", font=("Consolas", 11), wraplength=800)
        self.lbl_arr.pack(anchor=tk.W)

        # ===== [우측 영역: 코드 및 로그] =====
        tk.Label(self.right_col, text="🖥 현재 실행 중인 코드", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W)
        self.code_text = tk.Text(self.right_col, width=54, height=14, font=("Consolas", 10), bg="#2B2B2B", fg="#A9B7C6", padx=5, pady=5)
        self.code_text.pack(fill=tk.X)
        self.code_text.tag_config("highlight", background="#4B4D4D", foreground="#FFFFFF", font=("Consolas", 10, "bold"))
        self.code_text.config(state=tk.DISABLED) 
        
        self.tooltip = ToolTip(self.code_text)
        self.code_text.bind("<Motion>", self.on_code_hover)
        self.code_text.bind("<Leave>", lambda e: self.tooltip.hidetip())
        
        tk.Label(self.right_col, text="📜 스텝 실행 로그", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.log_text = ScrolledText(self.right_col, width=54, height=18, font=("맑은 고딕", 10), bg="#F5F5F5")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # ===== [하단 영역: 시각화 제어부] =====
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.control_frame = tk.Frame(self.bottom_frame)
        self.control_frame.pack()

        self.btn_play_pause = tk.Button(self.control_frame, text="▶ 재생", font=("맑은 고딕", 11, "bold"), width=12, bg="#4CAF50", fg="white", command=self.toggle_play_pause)
        self.btn_play_pause.grid(row=0, column=0, padx=5)

        self.btn_next_step = tk.Button(self.control_frame, text="⏭ 다음 스텝", font=("맑은 고딕", 11, "bold"), width=12, bg="#2196F3", fg="white", command=self.do_next_step)
        self.btn_next_step.grid(row=0, column=1, padx=5)
        
        # 뷰 모드 라디오 버튼 설정
        self.view_mode = tk.StringVar(value="array")
        self.mode_frame = tk.LabelFrame(self.bottom_frame, text="시각화 모드 선택", font=("맑은 고딕", 10, "bold"))
        self.mode_frame.pack(pady=5)
        
        tk.Radiobutton(self.mode_frame, text="배열 분할 모드 (이전과 유사)", variable=self.view_mode, value="array", command=lambda: self.draw_current_state(), font=("맑은 고딕", 10)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(self.mode_frame, text="재귀 트리 모드 (전체 구조 조망)", variable=self.view_mode, value="tree", command=lambda: self.draw_current_state(), font=("맑은 고딕", 10)).pack(side=tk.LEFT, padx=10)

        self.code_lines = []
        self.current_nodes = {}
        self.current_node_id = -1
        
        try:
            action, code_source, _, msg = next(self.generator)
            if action == "INIT_CODE":
                self.init_code_view(code_source)
        except StopIteration:
            pass

    def add_log(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def draw_array_split(self, nodes, reason, action, current_node_id):
        self.canvas.delete("all")
        if not nodes or current_node_id == -1: return

        # 1. 원본 배열 전체를 상단에 흐리게 표시
        max_bars_w = min(50, (self.canvas_width - 40 - (self.n - 1) * 8) // self.n)
        bx_w = max_bars_w
        gap = 8
        total_w = self.n * bx_w + (self.n - 1) * gap
        start_x = (self.canvas_width - total_w) // 2
        
        y_base_top = 100
        
        self.canvas.create_text(self.canvas_width // 2, 30, text="원본 배열", font=("맑은 고딕", 11, "bold"), fill="#757575")
        
        for idx, val in enumerate(self.arr):
            x1 = start_x + idx * (bx_w + gap)
            y1 = y_base_top - 30
            x2 = x1 + bx_w
            y2 = y_base_top
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#E0E0E0", outline="#BDBDBD", width=1)
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(val), font=("Consolas", 10), fill="#757575")

        # 2. 현재 작업 중인 노드(부분 배열)를 하단에 크게 표시
        cur_node = nodes.get(current_node_id)
        if cur_node:
            left = cur_node["left"]
            right = cur_node["right"]
            sub_len = right - left + 1
            
            self.canvas.create_text(self.canvas_width // 2, 170, text=f"현재 분할된 부분 배열 (인덱스 {left} ~ {right})", font=("맑은 고딕", 12, "bold"), fill="#1565C0")
            
            sub_start_x = start_x + left * (bx_w + gap)
            y_base_sub = 300
            
            for idx in range(left, right + 1):
                val = self.arr[idx]
                x1 = start_x + idx * (bx_w + gap)
                h = max(30, int((val / max(self.arr)) * 100)) if max(self.arr) > 0 else 30
                y1 = y_base_sub - h
                x2 = x1 + bx_w
                y2 = y_base_sub
                
                bg_col = "#BBDEFB"
                out_col = "#64B5F6"
                thicc = 2
                
                # 병합된 상태거나 Base Case인 경우
                if cur_node["status"] == "DONE":
                    if val == cur_node["val"]:
                        bg_col = "#C8E6C9" # 최댓값은 초록색
                        out_col = "#388E3C"
                        thicc = 3
                    else:
                        bg_col = "#E0E0E0" # 나머지는 회색
                        out_col = "#9E9E9E"

                # 분할 중임을 강조
                if "DIVIDE" in action and idx in (left, right):
                    bg_col = "#E1BEE7"
                    out_col = "#BA68C8"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_col, outline=out_col, width=thicc)
                self.canvas.create_text((x1+x2)/2, y1 - 15, text=str(val), font=("Consolas", 12, "bold"))
                self.canvas.create_text((x1+x2)/2, y2 + 15, text=f"[{idx}]", font=("Arial", 9))

        # 3. 말풍선
        if reason:
            bg_color = "#424242"
            if "CALL" in action: bg_color = "#1565C0"
            elif "BASE" in action: bg_color = "#E65100"
            elif "DIVIDE" in action: bg_color = "#6A1B9A"
            elif "MERGE" in action: bg_color = "#F57C00"
            elif "RETURN" in action: bg_color = "#2E7D32"
            
            t_id = self.canvas.create_text(self.canvas_width // 2, self.canvas_height - 30, text=reason, font=("맑은 고딕", 12, "bold"), fill="white", justify=tk.CENTER)
            bbox = self.canvas.bbox(t_id)
            if bbox:
                r_id = self.canvas.create_rectangle(bbox[0]-15, bbox[1]-8, bbox[2]+15, bbox[3]+8, fill=bg_color, outline="white", width=2)
                self.canvas.tag_lower(r_id, t_id)

    def draw_recursive_tree(self, nodes, reason, action):
        self.canvas.delete("all")
        if not nodes: return
        
        # ... (이전 코드 내용은 그대로 유지, 생략 부분 포함)
        depth_nodes = {}
        max_depth = 0
        for n_id, node in nodes.items():
            d = node["depth"]
            max_depth = max(max_depth, d)
            if d not in depth_nodes:
                depth_nodes[d] = []
            depth_nodes[d].append(node)
                
        node_coords = {}
        v_gap = 80 
        start_y = 60
        
        def assign_coords(n_id, x, y, x_offset):
            if n_id not in nodes: return
            node = nodes[n_id]
            node_coords[n_id] = (x, y)
            
            if node["child_l"] is not None:
                assign_coords(node["child_l"], x - x_offset, y + v_gap, max(x_offset * 0.5, 40))
            if node["child_r"] is not None:
                assign_coords(node["child_r"], x + x_offset, y + v_gap, max(x_offset * 0.5, 40))

        if 0 in nodes:
            assign_coords(0, self.canvas_width // 2, start_y, 200)

        for n_id, (nx, ny) in node_coords.items():
            node = nodes[n_id]
            
            if node["child_l"] is not None and node["child_l"] in node_coords:
                cx, cy = node_coords[node["child_l"]]
                line_col = "#BDBDBD"
                if nodes[node["child_l"]]["status"] == "COMPUTING": line_col = "#FF9800"
                elif nodes[node["child_l"]]["status"] == "DONE": line_col = "#4CAF50"
                self.canvas.create_line(nx, ny, cx, cy, fill=line_col, width=2)
                
            if node["child_r"] is not None and node["child_r"] in node_coords:
                cx, cy = node_coords[node["child_r"]]
                line_col = "#BDBDBD"
                if nodes[node["child_r"]]["status"] == "COMPUTING": line_col = "#FF9800"
                elif nodes[node["child_r"]]["status"] == "DONE": line_col = "#4CAF50"
                self.canvas.create_line(nx, ny, cx, cy, fill=line_col, width=2)

        for n_id, (nx, ny) in node_coords.items():
            node = nodes[n_id]
            
            bg_col = "#E0E0E0"
            out_col = "#9E9E9E"
            val_text = "?"
            
            if node["status"] == "COMPUTING":
                bg_col = "#FFF59D" 
                out_col = "#FBC02D"
            elif node["status"] == "DONE":
                bg_col = "#C8E6C9" 
                out_col = "#388E3C"
                val_text = str(node["val"])
                
            if "MERGE" in action and node["status"] == "COMPUTING":
                bg_col = "#FFCC80" 
                out_col = "#F57C00"
                
            rect_w = 40
            rect_h = 25
            self.canvas.create_rectangle(nx - rect_w, ny - rect_h, nx + rect_w, ny + rect_h, fill=bg_col, outline=out_col, width=2)
            
            range_text = f"[{node['left']}~{node['right']}]" if node['left'] != node['right'] else f"[{node['left']}]"
            self.canvas.create_text(nx, ny - 10, text=range_text, font=("Consolas", 10), fill="#424242")
            
            self.canvas.create_text(nx, ny + 8, text=f"Max:{val_text}", font=("Consolas", 11, "bold"), fill="#1A237E")

        if reason:
            bg_color = "#424242"
            if "CALL" in action: bg_color = "#1565C0"
            elif "BASE" in action: bg_color = "#E65100"
            elif "DIVIDE" in action: bg_color = "#6A1B9A"
            elif "MERGE" in action: bg_color = "#F57C00"
            elif "RETURN" in action: bg_color = "#2E7D32"
            
            t_id = self.canvas.create_text(self.canvas_width // 2, self.canvas_height - 30, text=reason, font=("맑은 고딕", 12, "bold"), fill="white", justify=tk.CENTER)
            bbox = self.canvas.bbox(t_id)
            if bbox:
                r_id = self.canvas.create_rectangle(bbox[0]-15, bbox[1]-8, bbox[2]+15, bbox[3]+8, fill=bg_color, outline="white", width=2)
                self.canvas.tag_lower(r_id, t_id)


    def init_code_view(self, code_source):
        self.code_lines = code_source
        self.code_text.config(state=tk.NORMAL)
        self.code_text.delete(1.0, tk.END)
        for line in code_source:
            self.code_text.insert(tk.END, line + "\n")
        self.code_text.config(state=tk.DISABLED)

    def highlight_code_line(self, line_index):
        if line_index < 0 or line_index >= len(self.code_lines): return
        self.code_text.config(state=tk.NORMAL)
        self.code_text.tag_remove("highlight", 1.0, tk.END)
        start_pos = f"{line_index + 1}.0"
        end_pos = f"{line_index + 1}.end"
        self.code_text.tag_add("highlight", start_pos, end_pos)
        self.code_text.see(start_pos) 
        self.code_text.config(state=tk.DISABLED)

    def toggle_play_pause(self):
        if self.is_finished: return

        self.is_paused = not self.is_paused
        if self.is_paused:
            self.btn_play_pause.config(text="▶ 재생", bg="#4CAF50")
            self.status_var.set("[일시정지 중]")
            self.add_log("⏸ 일시 정지")
        else:
            self.btn_play_pause.config(text="⏸ 일시정지", bg="#f44336")
            self.status_var.set("[자동 재생 중...]")
            self.add_log("▶ 자동 재생 시작")
            self.auto_step()

    def do_next_step(self):
        if self.is_finished: return
        if not self.is_paused: self.toggle_play_pause()
        self.execute_single_step()

    def auto_step(self):
        if not self.winfo_exists(): return
        if self.is_paused or self.is_finished: return 
        delay_used = self.execute_single_step()
        if not self.is_finished and delay_used is not None and self.winfo_exists():
            self.after(delay_used, lambda: self.auto_step())

    def execute_single_step(self):
        if not self.winfo_exists(): return None
        try:
            action, state, code_line, reason = next(self.generator)

            self.highlight_code_line(code_line)
            self.current_nodes = state["nodes"]
            self.current_node_id = state.get("current_node_id", -1)
            
            if "CALL_FUNC" in action:
                self.add_log("-----------------------------------------")
            
            self.add_log(f"{reason}")

            if not self.is_paused:
                self.status_var.set(f"[자동 진행 단계]")
            else:
                self.status_var.set(f"[일시 정지 대기중]")

            self.draw_current_state(reason, action)
                
            current_delay = self.delay
            if action in ["RETURN", "BASE_CASE", "FINISHED"]: 
                current_delay = int(self.delay * 1.5)
            elif action in ["DIVIDE_LEFT", "DIVIDE_RIGHT"]:
                current_delay = int(self.delay * 1.2)
            
            return current_delay
                
        except StopIteration:
            self.status_var.set("🏁 분할 정복 연산 완료! 🏁")
            self.is_finished = True
            
            self.btn_play_pause.config(state=tk.DISABLED, bg="gray")
            self.btn_next_step.config(state=tk.DISABLED, bg="gray")
            return None

    def draw_current_state(self, reason="", action=""):
        if self.view_mode.get() == "array":
            self.draw_array_split(self.current_nodes, reason, action, self.current_node_id)
        else:
            self.draw_recursive_tree(self.current_nodes, reason, action)

    def on_code_hover(self, event):
        index = self.code_text.index(f"@{event.x},{event.y}")
        word_start = self.code_text.index(f"{index} wordstart")
        word_end = self.code_text.index(f"{index} wordend")
        word = self.code_text.get(word_start, word_end).strip()
        
        desc = ""
        if word == "arr": desc = f"원본 배열 = {self.arr}"
        elif word == "left": desc = "left: 현재 쪼개진 배열의 맨 앞(왼쪽) 인덱스"
        elif word == "right": desc = "right: 현재 쪼개진 배열의 맨 뒤(오른쪽) 인덱스"
        elif word == "mid": desc = "mid: 배열을 두 덩이로 나누기 위한 중간 기준점 계산 수식"
        elif word == "max_left": desc = "max_left: 나눠진 부분 중 '왼쪽 그룹'의 최댓값을 저장하는 변수"
        elif word == "max_right": desc = "max_right: 나눠진 부분 중 '오른쪽 그룹'의 최댓값을 저장하는 변수"
        elif word == "max": desc = "max(): 파이썬 내장 함수 - 괄호 안의 두 인자 중 큰 값을 반환합니다."
        
        if desc: self.tooltip.showtip(desc, event.x_root, event.y_root)
        else: self.tooltip.hidetip()
