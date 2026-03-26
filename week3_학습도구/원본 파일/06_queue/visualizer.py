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

class QueueVisualizer(tk.Tk):
    def __init__(self, jobs, generator, delay=800):
        super().__init__()
        self.title("큐 (Queue) 자료구조 동작 시각화 - 프린터 대기열")
        self.jobs = jobs
        self.n = len(jobs)
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
        
        self.lbl_queue = tk.Label(self.var_frame, text=f"대기열 (queue): []", font=("Consolas", 11))
        self.lbl_queue.pack(anchor=tk.W)
        self.lbl_vars = tk.Label(self.var_frame, text="현재 작업(job): ? / 완료된 작업(processed): []", font=("Consolas", 11))
        self.lbl_vars.pack(anchor=tk.W)

        tk.Label(self.right_col, text="🖥 현재 실행 중인 코드", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W)
        self.code_text = tk.Text(self.right_col, width=54, height=14, font=("Consolas", 10), bg="#2B2B2B", fg="#A9B7C6", padx=5, pady=5)
        self.code_text.pack(fill=tk.X)
        self.code_text.tag_config("highlight", background="#4B4D4D", foreground="#FFFFFF", font=("Consolas", 10, "bold"))
        self.code_text.config(state=tk.DISABLED) 
        
        self.tooltip = ToolTip(self.code_text)
        self.code_text.bind("<Motion>", self.on_code_hover)
        self.code_text.bind("<Leave>", lambda e: self.tooltip.hidetip())
        self.current_vars = {}

        tk.Label(self.right_col, text="📜 스텝 실행 로그", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.log_text = ScrolledText(self.right_col, width=54, height=18, font=("맑은 고딕", 10), bg="#F5F5F5")
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

    def draw_queue_state(self, state, reason, action):
        self.canvas.delete("all")
        
        queue_arr = state.get("queue", [])
        processed = state.get("processed", [])
        current_job = state.get("current_job", None)
        
        # 1. 큐의 파이프 (수평) 그리기
        tube_w = 400
        tube_h = 70
        tube_start_x = self.canvas_width // 2 - tube_w // 2
        tube_start_y = 120
        
        # 위쪽 아래쪽 테두리 선 (양 끝이 뚫린 파이프 형태)
        self.canvas.create_line(tube_start_x, tube_start_y - tube_h//2, 
                                tube_start_x + tube_w, tube_start_y - tube_h//2, 
                                width=4, fill="#1976D2")
        self.canvas.create_line(tube_start_x, tube_start_y + tube_h//2, 
                                tube_start_x + tube_w, tube_start_y + tube_h//2, 
                                width=4, fill="#1976D2")
        
        self.canvas.create_text(self.canvas_width // 2, tube_start_y - tube_h//2 - 25, 
                                text="인쇄 대기열 큐 (Queue - FIFO 통로)", font=("맑은 고딕", 12, "bold"), fill="#1976D2")
        
        self.canvas.create_text(tube_start_x - 30, tube_start_y, text="Dequeue\n<- Pop", font=("맑은 고딕", 11, "bold"), fill="#E65100")
        self.canvas.create_text(tube_start_x + tube_w + 35, tube_start_y, text="Enqueue\nPush <-", font=("맑은 고딕", 11, "bold"), fill="#2E7D32")
        
        # 2. 파이프 안의 문서 렌더링
        box_w = 70
        box_h = 50
        gap = 10
        
        for idx, item in enumerate(queue_arr):
            # 큐의 왼쪽(index 0)이 파이프의 왼쪽 출구 쪽에 가깝게 위치
            x = tube_start_x + 20 + idx * (box_w + gap) + box_w // 2
            y = tube_start_y
            
            bg_col = "#BBDEFB"
            out_col = "#64B5F6"
            thicc = 2
            
            if "ENQUEUE" in action and idx == len(queue_arr) - 1:
                bg_col = "#C8E6C9"
                out_col = "#81C784"
                thicc = 3
                
            self.canvas.create_rectangle(x - box_w//2, y - box_h//2, x + box_w//2, y + box_h//2, 
                                         fill=bg_col, outline=out_col, width=thicc)
            self.canvas.create_text(x, y, text=item, font=("맑은 고딕", 11, "bold"), fill="#0D47A1")
            
        # 3. 현재 팝되어 처리중인 문서 표시 공간
        proc_x = self.canvas_width // 2
        proc_y = tube_start_y + 160
        
        self.canvas.create_rectangle(proc_x - 120, proc_y - 40, proc_x + 120, proc_y + 40, 
                                     fill="#F5F5F5", outline="#9E9E9E", dash=(4,4), width=2)
        self.canvas.create_text(proc_x, proc_y - 25, text="🖨 프린터 (현재 처리 중인 작업)", font=("맑은 고딕", 11, "bold"), fill="#424242")
        
        if current_job:
            bg_col = "#FFF9C4"
            out_col = "#FBC02D"
            if "PRINT" in action:
                bg_col = "#FFECB3"
                out_col = "#FFB300"
                
            self.canvas.create_rectangle(proc_x - 40, proc_y, proc_x + 40, proc_y + 35, 
                                         fill=bg_col, outline=out_col, width=2)
            self.canvas.create_text(proc_x, proc_y + 17, text=current_job, font=("맑은 고딕", 11, "bold"), fill="#F57C00")

        # 4. 애니메이션 효과 선 
        if "DEQUEUE" in action:
            self.canvas.create_line(tube_start_x, tube_start_y, proc_x - 40, proc_y, arrow=tk.LAST, width=3, fill="#E65100", dash=(2,2))
        elif "PROCESS_PRINT" in action:
            # 레이저나 처리 이펙트
            for i in range(-15, 20, 10):
                self.canvas.create_line(proc_x - 80, proc_y + 17 + i, proc_x - 50, proc_y + 17 + i, fill="#29B6F6", width=2)
        elif "PROCESS_DONE" in action:
            self.canvas.create_line(proc_x, proc_y + 35, proc_x, proc_y + 90, arrow=tk.LAST, width=3, fill="#66BB6A", dash=(2,2))

        # 5. 아래쪽: 완료된 작업(processed) 리스트 수납장
        done_start_x = self.canvas_width // 2 - (len(self.jobs) * 80) // 2
        done_y = proc_y + 110
        self.canvas.create_text(self.canvas_width // 2, done_y - 20, text="✅ 완료된 작업 (processed)", font=("맑은 고딕", 11, "bold"), fill="#212121")
        
        for idx, item in enumerate(processed):
            x = done_start_x + idx * (box_w + gap) + box_w // 2
            self.canvas.create_rectangle(x - box_w//2, done_y, x + box_w//2, done_y + box_h, 
                                         fill="#E8F5E9", outline="#81C784", width=2)
            self.canvas.create_text(x, done_y + box_h//2, text=item, font=("맑은 고딕", 10), fill="#388E3C")


        # 말풍선
        if reason:
            bg_color = "#424242"
            if "ENQUEUE" in action: bg_color = "#2E7D32"
            elif "DEQUEUE" in action: bg_color = "#E65100"
            elif "PROCESS" in action: bg_color = "#0277BD"
            
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
        current_job = state.get('current_job', None)
        queue_arr = state.get('queue', [])
        processed = state.get('processed', [])
        
        self.lbl_queue.config(text=f"대기열 (queue): {queue_arr}")
        self.lbl_vars.config(text=f"현재 작업(job): {current_job if current_job else '없음'} / 완료된 작업(processed): {processed}")

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
            
            if action in ["CHECK_WHILE"]:
                self.add_log("-----------------------------------------")
            
            self.add_log(f"{reason}")

            if not self.is_paused:
                self.status_var.set(f"[자동 진행 단계]")
            else:
                self.status_var.set(f"[일시 정지 대기중]")

            self.draw_queue_state(state, reason, action=action)
                
            current_delay = self.delay
            if action in ["FINISHED"]: 
                current_delay = int(self.delay * 2.0)
            elif "PRE" in action or "DONE" in action:
                current_delay = int(self.delay * 1.5)
            elif action == "PROCESS_PRINT":
                current_delay = int(self.delay * 2.5) # 인쇄는 조금 더 길게
            
            return current_delay
                
        except StopIteration:
            self.status_var.set("🏁 큐 시뮬레이터 (프린터 대기열) 종료! 🏁")
            self.add_log("🏁 프린터 작업 처리가 모두 완료되었습니다.")
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
        if word == "deque": desc = f"deque: collections 모듈에서 제공하는 양방향 큐 자료구조입니다."
        elif word == "queue": desc = f"queue: FIFO(선입선출) 구조. 현재 대기 상태 = {cv.get('queue', [])}"
        elif word == "job": desc = f"job: 현재 파이프에서 빠져나와 프린터가 처리 중인 문서"
        elif word == "processed": desc = f"processed: 인쇄를 마치고 반환을 위해 모인 배열(리스트)"
        elif word == "popleft": desc = f"popleft(): 큐의 가장 왼쪽 끝(가장 먼저 들어온 부분)에 있는 요소를 꺼내옵니다."

        if desc: self.tooltip.showtip(desc, event.x_root, event.y_root)
        else: self.tooltip.hidetip()
