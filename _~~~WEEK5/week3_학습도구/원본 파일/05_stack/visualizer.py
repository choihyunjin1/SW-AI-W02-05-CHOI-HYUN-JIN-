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

class StackVisualizer(tk.Tk):
    def __init__(self, s, generator, delay=600):
        super().__init__()
        self.title("스택 (Stack) 자료구조 동작 시각화 - 괄호 검사")
        self.s = s
        self.n = len(s)
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
        self.canvas_height = 550
        self.canvas = tk.Canvas(self.left_col, width=self.canvas_width, height=self.canvas_height, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.canvas.pack(pady=5)
        
        self.status_var = tk.StringVar(value="초기화 중...")
        tk.Label(self.left_col, textvariable=self.status_var, font=("맑은 고딕", 12, "bold"), fg="blue").pack(pady=5)

        self.var_frame = tk.LabelFrame(self.left_col, text="💡 현재 변수 상태(State Monitor)", font=("맑은 고딕", 11, "bold"), fg="#D32F2F")
        self.var_frame.pack(fill=tk.X, pady=5, ipadx=5, ipady=5)
        
        self.lbl_str = tk.Label(self.var_frame, text=f"검사 대상 문자열(s): {self.s}", font=("Consolas", 11))
        self.lbl_str.pack(anchor=tk.W)
        self.lbl_vars = tk.Label(self.var_frame, text="현재 인덱스(i): ? / 현재 문자(char): ? / 스택 개수(len): ?", font=("Consolas", 11))
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
        self.log_text = ScrolledText(self.right_col, width=54, height=14, font=("맑은 고딕", 10), bg="#F5F5F5")
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

    def draw_stack_state(self, state, reason, action):
        self.canvas.delete("all")
        
        stack = state.get("stack", [])
        idx = state.get("idx", -1)
        
        # 1. 윗부분: 원본 문자열 순회 표시
        str_start_x = self.canvas_width // 2 - (self.n * 35) // 2
        str_y = 60
        
        self.canvas.create_text(self.canvas_width // 2, 20, text="입력 문자열 (String) - 순회 중", font=("맑은 고딕", 11, "bold"), fill="#616161")
        
        for i, char in enumerate(self.s):
            x = str_start_x + i * 35
            
            bg_col = "#E0E0E0"
            out_col = "#BDBDBD"
            font_col = "#757575"
            thicc = 1
            
            if i == idx:
                bg_col = "#FFF59D" # 현재 검사 위치 노란색
                out_col = "#FBC02D"
                font_col = "#212121"
                thicc = 3
            elif i < idx:
                bg_col = "#F5F5F5" # 이미 지나간 곳
                out_col = "#E0E0E0"
                font_col = "#BDBDBD"
                
            self.canvas.create_rectangle(x - 15, str_y - 20, x + 15, str_y + 20, fill=bg_col, outline=out_col, width=thicc)
            self.canvas.create_text(x, str_y, text=char, font=("Consolas", 14, "bold"), fill=font_col)
            self.canvas.create_text(x, str_y + 30, text=str(i), font=("Arial", 9), fill="#9E9E9E")
            
            if i == idx:
                self.canvas.create_polygon(x, str_y - 40, x - 10, str_y - 30, x + 10, str_y - 30, fill="#E65100") # 포인터 화살표

        # 2. 중간 부분: 스택 (LIFO 통 구조) 그리기
        bucket_w = 120
        bucket_h = 250
        bucket_b_y = 400
        bucket_x = self.canvas_width // 2
        
        # U자형 컵 (스택) 그리기
        self.canvas.create_line(bucket_x - bucket_w//2, bucket_b_y - bucket_h, 
                                bucket_x - bucket_w//2, bucket_b_y, 
                                bucket_x + bucket_w//2, bucket_b_y, 
                                bucket_x + bucket_w//2, bucket_b_y - bucket_h, 
                                width=4, fill="#1976D2")
        
        self.canvas.create_text(bucket_x, bucket_b_y + 25, text="스택 (Stack - LIFO)", font=("맑은 고딕", 12, "bold"), fill="#1976D2")
        
        # 스택 내부 요소 박스 그리기
        box_h = 35
        # 스택 최대 용량 초과 시 컵 바깥으로 삐져나갈 수 있으므로 제한적으로 위치 계산
        max_visible_len = bucket_h // box_h
        
        # 바닥부터 채워넣음
        for j, item in enumerate(stack):
            b_x = bucket_x
            b_y = bucket_b_y - 2 - (j * box_h) - box_h//2
            
            # 방금 들어오거나 나간 요소 효과 처리
            bg_col = "#BBDEFB"
            out_col = "#64B5F6"
            thicc = 2
            
            is_top = (j == len(stack) - 1)
            
            if "PUSH_DONE" in action and is_top:
                bg_col = "#81C784" # Push 성공 초록
                out_col = "#388E3C"
                thicc = 3
            
            self.canvas.create_rectangle(b_x - bucket_w//2 + 5, b_y - box_h//2 + 2, 
                                         b_x + bucket_w//2 - 5, b_y + box_h//2 - 2, 
                                         fill=bg_col, outline=out_col, width=thicc)
            self.canvas.create_text(b_x, b_y, text=item, font=("Consolas", 14, "bold"), fill="#1565C0")
            
            if is_top:
                self.canvas.create_text(b_x - bucket_w//2 - 25, b_y, text="<- Top", font=("Consolas", 10, "bold"), fill="#D32F2F")
                
        # 3. 애니메이션 보조 시각화 공간 (Push 전 대기, Pop 된 후 상태)
        # Push_pre, Pop_pre, Pop_done 에 따라서 컵 바깥 상단에 무언가 나타나게 함
        if "PUSH_PRE" in action:
            p_y = bucket_b_y - bucket_h - 40
            self.canvas.create_rectangle(bucket_x - bucket_w//2 + 5, p_y - box_h//2 + 2, 
                                         bucket_x + bucket_w//2 - 5, p_y + box_h//2 - 2, 
                                         fill="#A5D6A7", outline="#4CAF50", width=3, dash=(4,4))
            self.canvas.create_text(bucket_x, p_y, text="(", font=("Consolas", 14, "bold"), fill="#2E7D32")
            self.canvas.create_text(bucket_x + bucket_w//2 + 40, p_y, text="Push ↓", font=("맑은 고딕", 12, "bold"), fill="#2E7D32")
            
        elif "POP_PRE" in action:
            # 탑에 있는 놈을 빨갛게 강조
            pass # 위에서 탑 요소 그릴때 해줘도 됨 (여기선 생략)
            
        elif "POP_DONE" in action:
            p_y = bucket_b_y - bucket_h - 40
            self.canvas.create_rectangle(bucket_x - bucket_w//2 + 5, p_y - box_h//2 + 2, 
                                         bucket_x + bucket_w//2 - 5, p_y + box_h//2 - 2, 
                                         fill="#FFCDD2", outline="#EF5350", width=3, dash=(4,4))
            self.canvas.create_text(bucket_x, p_y, text="(", font=("Consolas", 14, "bold"), fill="#C62828")
            self.canvas.create_text(bucket_x + bucket_w//2 + 40, p_y, text="Pop ↑", font=("맑은 고딕", 12, "bold"), fill="#C62828")
            

        # 말풍선
        if reason:
            bg_color = "#424242"
            if "PUSH" in action: bg_color = "#2E7D32"
            elif "POP" in action: bg_color = "#C62828"
            elif "ERROR" in action or "FALSE" in action: bg_color = "#D32F2F"
            elif "TRUE" in action: bg_color = "#1565C0"
            
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
        idx = state.get('idx', -1)
        char = state.get('char', '')
        stack = state.get('stack', [])
        
        self.lbl_vars.config(text=f"현재 인덱스(i): {idx if idx != -1 else '?'} / 현재 문자(char): '{char}' / 스택 개수(len): {len(stack)}")

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
            
            if action in ["LOOP_NEXT", "LOOP_END"]:
                self.add_log("-----------------------------------------")
            
            # 너무 긴 로그 방지
            if "DONE" not in action:
                self.add_log(f"{reason}")

            if not self.is_paused:
                self.status_var.set(f"[자동 진행 단계]")
            else:
                self.status_var.set(f"[일시 정지 대기중]")

            self.draw_stack_state(state, reason, action=action)
                
            current_delay = self.delay
            if action in ["FINISHED_TRUE", "FINISHED_FALSE", "ERROR_EMPTY"]: 
                current_delay = int(self.delay * 2.0)
            elif "PRE" in action or "DONE" in action:
                current_delay = int(self.delay * 1.5)
            elif "CHECK" in action:
                current_delay = int(self.delay * 0.8)
            
            return current_delay
                
        except StopIteration:
            self.status_var.set("🏁 스택 동작 및 유효성 검사 완료! 🏁")
            self.add_log("🏁 알고리즘 종료.")
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
        if word == "s": desc = f"검사 대상 문자열 = {self.s}"
        elif word == "stack": desc = f"스택: LIFO(후입선출) 구조의 배열. 현재 탑({cv.get('stack', [])})"
        elif word == "char": desc = f"char: 문자열에서 하나씩 빼서 확인 중인 현재 문자"
        elif word == "append": desc = f"append(): 스택의 가장 위에 새로운 요소를 추가(Push) 합니다."
        elif word == "pop": desc = f"pop(): 스택의 가장 위에 있는 최신 요소를 삭제(제거) 후 반환 합니다."

        if desc: self.tooltip.showtip(desc, event.x_root, event.y_root)
        else: self.tooltip.hidetip()
