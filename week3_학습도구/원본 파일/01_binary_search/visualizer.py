import tkinter as tk
from tkinter.scrolledtext import ScrolledText

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

class BinarySearchVisualizer(tk.Tk):
    def __init__(self, arr, target, generator, delay=800):
        super().__init__()
        self.title("이분 탐색 (Binary Search) 시각화 학습 도구")
        self.arr = arr
        self.target = target
        self.n = len(arr)
        self.max_val = max(arr) if arr else 1
        self.generator = generator
        self.delay = delay 
        
        self.is_paused = True   
        self.is_finished = False 
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.left_col = tk.Frame(self.top_frame)
        self.left_col.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.right_col = tk.Frame(self.top_frame)
        self.right_col.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        
        self.canvas_width = 800
        self.canvas_height = 450
        self.canvas = tk.Canvas(self.left_col, width=self.canvas_width, height=self.canvas_height, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.canvas.pack(pady=5)
        
        self.status_var = tk.StringVar(value="초기화 중...")
        tk.Label(self.left_col, textvariable=self.status_var, font=("맑은 고딕", 12, "bold"), fg="blue").pack(pady=5)

        self.var_frame = tk.LabelFrame(self.left_col, text="💡 현재 변수 상태(State Monitor)", font=("맑은 고딕", 11, "bold"), fg="#D32F2F")
        self.var_frame.pack(fill=tk.X, pady=5, ipadx=5, ipady=5)
        
        self.lbl_pointers = tk.Label(self.var_frame, text="left: ? / right: ? / mid: ?", font=("Consolas", 11))
        self.lbl_pointers.pack(anchor=tk.W)
        self.lbl_vars = tk.Label(self.var_frame, text=f"target: {self.target} / 현재 배열 탐색 대상 수: {self.n}", font=("Consolas", 11))
        self.lbl_vars.pack(anchor=tk.W)

        tk.Label(self.right_col, text="🖥 현재 실행 중인 코드", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W)
        self.code_text = tk.Text(self.right_col, width=54, height=18, font=("Consolas", 10), bg="#2B2B2B", fg="#A9B7C6", padx=5, pady=5)
        self.code_text.pack(fill=tk.X)
        self.code_text.tag_config("highlight", background="#4B4D4D", foreground="#FFFFFF", font=("Consolas", 10, "bold"))
        self.code_text.config(state=tk.DISABLED) 
        
        self.tooltip = ToolTip(self.code_text)
        self.code_text.bind("<Motion>", self.on_code_hover)
        self.code_text.bind("<Leave>", lambda e: self.tooltip.hidetip())
        self.current_vars = {}

        tk.Label(self.right_col, text="📜 스텝 실행 로그", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.log_text = ScrolledText(self.right_col, width=54, height=12, font=("맑은 고딕", 10), bg="#F5F5F5")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.control_frame = tk.Frame(self.bottom_frame)
        self.control_frame.pack()

        self.btn_play_pause = tk.Button(self.control_frame, text="▶ 재생", font=("맑은 고딕", 11, "bold"), width=12, bg="#4CAF50", fg="white", command=self.toggle_play_pause)
        self.btn_play_pause.grid(row=0, column=0, padx=5)

        self.btn_next_step = tk.Button(self.control_frame, text="⏭ 다음 스텝", font=("맑은 고딕", 11, "bold"), width=12, bg="#2196F3", fg="white", command=self.do_next_step)
        self.btn_next_step.grid(row=0, column=1, padx=5)

        self.code_lines = []
        
        try:
            action, code_source, _, msg = next(self.generator)
            if action == "INIT_CODE":
                self.init_code_view(code_source)
                self.draw_arrays(self.arr, self.target, 0, self.n - 1, -1, msg)
        except StopIteration:
            pass

    def add_log(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def draw_arrays(self, arr, target, left, right, mid, reason, action=""):
        self.canvas.delete("all")
        if not arr: return
        
        max_bars_w = min(60, (self.canvas_width - 40 - (self.n - 1) * 8) // self.n)
        bx_w = max_bars_w
        gap = 8
        total_w = self.n * bx_w + (self.n - 1) * gap
        start_x = (self.canvas_width - total_w) // 2
        
        max_h = 240
        y_base = max_h + 80
        
        self.canvas.create_text(self.canvas_width // 2, 30, text=f"🔍 찾을 값 (Target): {target}", font=("맑은 고딕", 14, "bold"), fill="#E65100")
        
        # 탐색 범위를 감싸는 직사각형 배경그리기
        if left != -1 and right != -1 and left <= right:
            rx1 = start_x + left * (bx_w + gap) - gap//2
            rx2 = start_x + right * (bx_w + gap) + bx_w + gap//2
            self.canvas.create_rectangle(rx1, 60, rx2, y_base + 60, fill="#E3F2FD", outline="#90CAF9", dash=(4, 4))
            self.canvas.create_text((rx1+rx2)/2, 75, text=f"탐색 범위 (left={left} ~ right={right})", font=("맑은 고딕", 10, "bold"), fill="#1565C0")

        for idx, val in enumerate(arr):
            x1 = start_x + idx * (bx_w + gap)
            h = max(20, int((val / self.max_val) * max_h)) if self.max_val > 0 else 20
            y1 = y_base - h
            x2 = x1 + bx_w
            y2 = y_base
            
            # 탐색 범위 밖은 회색 (비활성화 느낌)
            bg_col = "#E0E0E0"
            outline_col = "#BDBDBD"
            thicc = 1
            text_color = "#9E9E9E"
            
            if left <= idx <= right:
                bg_col = "#BBDEFB" # 범위 안 기본색
                outline_col = "#64B5F6"
                thicc = 2
                text_color = "black"
                
            if idx == mid and mid != -1:
                bg_col = "#FFF59D" # 노란색
                outline_col = "#FBC02D"
                thicc = 3
                text_color = "black"
                
            if "FOUND" in action and idx == mid:
                bg_col = "#A5D6A7" # 초록색
                outline_col = "#4CAF50"
                thicc = 3
                text_color = "white"
                
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_col, outline=outline_col, width=thicc)
            self.canvas.create_text((x1+x2)/2, y1 - 12, text=str(val), font=("Consolas", 12, "bold"), fill=text_color)
            self.canvas.create_text((x1+x2)/2, y2 + 15, text=f"[{idx}]", font=("Arial", 9), fill=text_color)
            
            pointers = []
            if idx == left: pointers.append("left")
            if idx == right: pointers.append("right")
            if idx == mid and left != right: pointers.append("mid")
            elif idx == mid and left == right: pointers.append("mid(L,R)") # 겹칠 때
            
            if pointers:
                # 'mid(L,R)' 처럼 처리했으므로 필터링 후 출력
                p_text = "\n".join([p for p in pointers if "mid" in p] or pointers) 
                
                f_color = "#E65100" if idx == mid else "#1565C0"
                y_offset = 35
                for p in pointers:
                    self.canvas.create_text((x1+x2)/2, y2 + y_offset, text=p, font=("Consolas", 11, "bold"), fill=f_color)
                    y_offset += 15

        if reason:
            bg_color = "#424242"
            if "FOUND" in action: bg_color = "#2E7D32"
            elif "NOT_FOUND" in action: bg_color = "#D32F2F"
            elif "CALC_MID" in action: bg_color = "#F57C00"
            elif "UPDATE" in action: bg_color = "#6A1B9A"
            
            t_id = self.canvas.create_text(self.canvas_width // 2, max_h + 170, text=reason, font=("맑은 고딕", 12, "bold"), fill="white", justify=tk.CENTER)
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

    def update_vars(self, state):
        left = state.get('left', -1)
        right = state.get('right', -1)
        mid = state.get('mid', -1)
        
        self.lbl_pointers.config(text=f"현재 포인터:: left: {left if left != -1 else '?'} / right: {right if right != -1 else '?'} / mid: {mid if mid != -1 else '?'}")
        
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

            self.current_vars = state
            self.highlight_code_line(code_line)
            self.update_vars(state)
            
            self.add_log(f"[{action}] {reason}")

            if not self.is_paused:
                self.status_var.set(f"[자동 진행 단계]")
            else:
                self.status_var.set(f"[일시 정지 대기중]")

            self.draw_arrays(
                state.get("arr", []), 
                state.get("target", -1), 
                state.get("left", -1), 
                state.get("right", -1), 
                state.get("mid", -1), 
                reason, 
                action=action
            )
                
            current_delay = self.delay
            if action in ["FOUND", "NOT_FOUND"]: 
                current_delay = int(self.delay * 2.0)
            elif "COMPARE" in action:
                current_delay = int(self.delay * 1.5)
            
            return current_delay
                
        except StopIteration:
            self.status_var.set("🏁 탐색 완료! 🏁")
            self.is_finished = True
            
            self.btn_play_pause.config(state=tk.DISABLED, bg="gray")
            self.btn_next_step.config(state=tk.DISABLED, bg="gray")
            return None

    def on_code_hover(self, event):
        index = self.code_text.index(f"@{event.x},{event.y}")
        word_start = self.code_text.index(f"{index} wordstart")
        word_end = self.code_text.index(f"{index} wordend")
        word = self.code_text.get(word_start, word_end).strip()
        
        cv = self.current_vars
        desc = ""
        if word == "arr": desc = f"arr (현재 배열 원소)\n{cv.get('arr', '?')}"
        elif word == "target": desc = f"target (찾는 값) = {cv.get('target', '?')}"
        elif word == "left": desc = f"left (탐색 범위 시작 인덱스) = {cv.get('left', '?')}"
        elif word == "right": desc = f"right (탐색 범위 끝 인덱스) = {cv.get('right', '?')}"
        elif word == "mid": desc = f"mid (현재 탐색할 중간 인덱스) = {cv.get('mid', '?')}"

        if desc: self.tooltip.showtip(desc, event.x_root, event.y_root)
        else: self.tooltip.hidetip()
