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

class MergeSortVisualizer(tk.Tk):
    def __init__(self, arr, generator, delay=500):
        super().__init__()
        self.title("병합 정렬 (Merge Sort) 알고리즘 학습 도구")
        self.original_arr = arr.copy()
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
        
        self.canvas_width = 850
        self.canvas_height = 550
        self.canvas = tk.Canvas(self.left_col, width=self.canvas_width, height=self.canvas_height, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.canvas.pack(pady=5)
        
        self.status_var = tk.StringVar(value="초기화 중...")
        tk.Label(self.left_col, textvariable=self.status_var, font=("맑은 고딕", 12, "bold"), fg="blue").pack(pady=5)

        self.var_frame = tk.LabelFrame(self.left_col, text="💡 현재 변수 상태(State Monitor)", font=("맑은 고딕", 11, "bold"), fg="#D32F2F")
        self.var_frame.pack(fill=tk.X, pady=5, ipadx=5, ipady=5)
        
        self.lbl_pointers = tk.Label(self.var_frame, text="부분 트리 인덱스:: left: ? / mid: ? / right: ?", font=("Consolas", 11))
        self.lbl_pointers.pack(anchor=tk.W)
        self.lbl_vars = tk.Label(self.var_frame, text="병합 임시 배열 위치:: i: ? / j: ? / 원본 복사 위치 k: ?", font=("Consolas", 11))
        self.lbl_vars.pack(anchor=tk.W)

        tk.Label(self.right_col, text="🖥 현재 실행 중인 코드", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W)
        self.code_text = tk.Text(self.right_col, width=56, height=25, font=("Consolas", 10), bg="#2B2B2B", fg="#A9B7C6", padx=5, pady=5)
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
        except StopIteration:
            pass

    def add_log(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def draw_arrays(self, state, reason, action):
        self.canvas.delete("all")
        
        arr = state.get("arr", [])
        if not arr: return
        
        left = state.get("left", -1)
        mid = state.get("mid", -1)
        right = state.get("right", -1)
        left_arr = state.get("left_arr", None)
        right_arr = state.get("right_arr", None)
        pt_i = state.get("i", -1)
        pt_j = state.get("j", -1)
        pt_k = state.get("k", -1)
        
        max_bars_w = min(40, (self.canvas_width - 40 - (self.n - 1) * 6) // self.n)
        bx_w = max_bars_w
        gap = 6
        total_w = self.n * bx_w + (self.n - 1) * gap
        start_x = (self.canvas_width - total_w) // 2
        
        max_h = 150
        y_base_main = 230
        
        self.canvas.create_text(start_x, y_base_main - max_h - 30, text="원본/메인 배열 (arr)", font=("맑은 고딕", 11, "bold"), fill="#424242", anchor=tk.W)

        # 현재 쪼개거나 합치고 있는 범위 박스 스케치
        if left != -1 and right != -1:
            rx1 = start_x + left * (bx_w + gap) - gap//2
            rx2 = start_x + right * (bx_w + gap) + bx_w + gap//2
            self.canvas.create_rectangle(rx1, y_base_main - max_h - 10, rx2, y_base_main + 50, fill="#f3ebf8", outline="#d1baf0", dash=(4, 4))
            self.canvas.create_text((rx1+rx2)/2, y_base_main - max_h + 5, text=f"분할/병합 범위 ({left}~{right})", font=("맑은 고딕", 9, "bold"), fill="#673ab7")

        for idx, val in enumerate(arr):
            x1 = start_x + idx * (bx_w + gap)
            h = max(15, int((val / self.max_val) * max_h)) if self.max_val > 0 else 15
            y1 = y_base_main - h
            x2 = x1 + bx_w
            y2 = y_base_main
            
            bg_col = "#E0E0E0" 
            outline_col = "#BDBDBD"
            thicc = 1
            
            if left <= idx <= right:
                bg_col = "#BBDEFB"
                outline_col = "#64B5F6"
                
            if idx == pt_k and "MERGE" not in action and pt_k != -1:
                bg_col = "#FFCDD2" # 병합하여 복사하려는 대상 위치 (분홍)
                outline_col = "#E57373"
                thicc = 2
                
            if action in ["COPY_REMAIN_L", "COPY_REMAIN_R", "MOVE_POINTER_L", "MOVE_POINTER_R"] and idx == (pt_k - 1) and pt_k > 0:
                # 방금 막 추가된 위치 강조 (초록색계열)
                bg_col = "#A5D6A7"
                outline_col = "#4CAF50"
                thicc = 2

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_col, outline=outline_col, width=thicc)
            self.canvas.create_text((x1+x2)/2, y1 - 10, text=str(val), font=("Consolas", 10))
            self.canvas.create_text((x1+x2)/2, y2 + 15, text=f"[{idx}]", font=("Arial", 8))
            
            if idx == pt_k and left_arr is not None:
                self.canvas.create_text((x1+x2)/2, y2 + 35, text="k", font=("Consolas", 10, "bold"), fill="#D32F2F")

        # 임시 보조 배열 (left_arr, right_arr) 그리기 - 병합 시에만 등장
        if left_arr is not None and right_arr is not None:
            y_base_temp = 430
            self.canvas.create_text(start_x, y_base_temp - max_h - 30, text="병합용 분할 복사 배열 (left_arr, right_arr)", font=("맑은 고딕", 11, "bold"), fill="#424242", anchor=tk.W)

            # Left Array
            left_total_w = len(left_arr) * bx_w + max(0, len(left_arr) - 1) * gap
            left_start_x = start_x + left * (bx_w + gap)
            
            for idx, val in enumerate(left_arr):
                x1 = left_start_x + idx * (bx_w + gap)
                h = max(15, int((val / self.max_val) * max_h)) if self.max_val > 0 else 15
                y1 = y_base_temp - h
                x2 = x1 + bx_w
                y2 = y_base_temp
                
                bg_col = "#FFF9C4" # 연노랑
                out_col = "#FFF176"
                thicc = 1
                
                if idx == pt_i:
                    bg_col = "#FFF176"
                    out_col = "#FBC02D"
                    thicc = 3
                elif idx < pt_i:
                    # 이미 처리된 원소는 회색 처리
                    bg_col = "#F5F5F5"
                    out_col = "#E0E0E0"
                    
                if "MERGE_LEFT" in action and idx == pt_i:
                    bg_col = "#FFB74D" # 선택 주황색
                    out_col = "#F57C00"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_col, outline=out_col, width=thicc)
                self.canvas.create_text((x1+x2)/2, y1 - 10, text=str(val), font=("Consolas", 10))
                
                if idx == pt_i:
                    self.canvas.create_text((x1+x2)/2, y2 + 15, text="i", font=("Consolas", 11, "bold"), fill="#F57C00")

            # Right Array
            right_start_x = left_start_x + left_total_w + 40 # 두 배열 사이 간격을 좀 더 띄움
            
            self.canvas.create_line(right_start_x - 20, y_base_temp - max_h, right_start_x - 20, y_base_temp, dash=(2, 2), fill="#9E9E9E")
            
            for idx, val in enumerate(right_arr):
                x1 = right_start_x + idx * (bx_w + gap)
                h = max(15, int((val / self.max_val) * max_h)) if self.max_val > 0 else 15
                y1 = y_base_temp - h
                x2 = x1 + bx_w
                y2 = y_base_temp
                
                bg_col = "#C8E6C9" # 연초록
                out_col = "#A5D6A7"
                thicc = 1
                
                if idx == pt_j:
                    bg_col = "#A5D6A7"
                    out_col = "#4CAF50"
                    thicc = 3
                elif idx < pt_j:
                    # 처리된 원소는 회색
                    bg_col = "#F5F5F5"
                    out_col = "#E0E0E0"
                    
                if "MERGE_RIGHT" in action and idx == pt_j:
                    bg_col = "#81C784" # 선택 초록색
                    out_col = "#388E3C"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_col, outline=out_col, width=thicc)
                self.canvas.create_text((x1+x2)/2, y1 - 10, text=str(val), font=("Consolas", 10))
                
                if idx == pt_j:
                    self.canvas.create_text((x1+x2)/2, y2 + 15, text="j", font=("Consolas", 11, "bold"), fill="#388E3C")


        # 말풍선
        if reason:
            bg_color = "#424242"
            if "DIVIDE" in action: bg_color = "#1565C0"
            elif "MERGE_L" in action or "MERGE_R" in action: bg_color = "#E65100"
            elif "COPY" in action: bg_color = "#2E7D32"
            
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

    def update_vars(self, state):
        left = state.get('left', -1)
        mid = state.get('mid', -1)
        right = state.get('right', -1)
        i = state.get('i', -1)
        j = state.get('j', -1)
        k = state.get('k', -1)
        
        self.lbl_pointers.config(text=f"부분 트리 인덱스:: left: {left if left != -1 else '?'} / mid: {mid if mid != -1 else '?'} / right: {right if right != -1 else '?'}")
        self.lbl_vars.config(text=f"병합 배열 위치:: i: {i if i != -1 else '?'} / j: {j if j != -1 else '?'} / 원본 복사 위치 k: {k if k != -1 else '?'}")

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
            
            if action in ["DIVIDE_LEFT", "DIVIDE_RIGHT", "CALL_MERGE"]:
                self.add_log("-----------------------------------------")
            log_txt = f"{reason}"
            self.add_log(log_txt)

            if not self.is_paused:
                self.status_var.set(f"[자동 진행 단계]")
            else:
                self.status_var.set(f"[일시 정지 대기중]")

            self.draw_arrays(state, reason, action=action)
                
            current_delay = self.delay
            if action in ["COPY_REMAIN_L", "COPY_REMAIN_R", "MOVE_POINTER_L", "MOVE_POINTER_R"]: 
                current_delay = int(self.delay * 1.5)
            elif action in ["DIVIDE_LEFT", "DIVIDE_RIGHT"]:
                current_delay = int(self.delay * 1.2)
            elif "COMPARE" in action:
                current_delay = int(self.delay * 0.8)
            
            return current_delay
                
        except StopIteration:
            self.status_var.set("🏁 병합 정렬 완료! 🏁")
            self.add_log("🏁 배열 정렬이 성공적으로 완료되었습니다.")
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
        if word == "arr": desc = f"원본 배열"
        elif word == "left_arr": desc = f"left_arr: 병합 대상인 왼쪽 절반 구간 복사본"
        elif word == "right_arr": desc = f"right_arr: 병합 대상인 오른쪽 절반 구간 복사본"
        elif word == "i": desc = f"i: 왼쪽 임시 배열(left_arr) 순회 및 선택 위치"
        elif word == "j": desc = f"j: 오른쪽 임시 배열(right_arr) 순회 및 선택 위치"
        elif word == "k": desc = f"k: 원본 배열(arr) 상에서 값을 덧어씌울 실제 위치"
        elif word == "left": desc = f"left: 정렬 범위 시작 인덱스"
        elif word == "right": desc = f"right: 정렬 범위 끝 인덱스"
        elif word == "mid": desc = f"mid: 영역을 둘로 나눌 중간 기준 인덱스"

        if desc: self.tooltip.showtip(desc, event.x_root, event.y_root)
        else: self.tooltip.hidetip()
