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

class PriorityQueueVisualizer(tk.Tk):
    def __init__(self, patients, generator, delay=900):
        super().__init__()
        self.title("우선순위 큐 (Priority Queue / Min-Heap) 시각화 - 응급실 환자")
        self.patients = patients
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
        
        self.lbl_heap = tk.Label(self.var_frame, text=f"힙 배열(heap): []", font=("Consolas", 11))
        self.lbl_heap.pack(anchor=tk.W)
        self.lbl_vars = tk.Label(self.var_frame, text="현재 타겟: ? / 비교 대상(부모,자식 등): ?", font=("Consolas", 11))
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

    def draw_heap_state(self, state, reason, action):
        self.canvas.delete("all")
        
        heap = state.get("heap", [])
        processed = state.get("processed", [])
        
        c_curr = state.get("curr", -1)
        c_parent = state.get("parent", -1)
        c_left = state.get("left", -1)
        c_right = state.get("right", -1)
        c_sm = state.get("smallest", -1)
        
        # 1. 탑 영역: 힙 트리 그리기
        self.canvas.create_text(self.canvas_width // 2, 20, text="우선순위 큐 힙 트리 구조 (Min-Heap Tree)", font=("맑은 고딕", 11, "bold"), fill="#616161")
        
        if heap:
            def draw_node(index, x, y, dx):
                if index >= len(heap):
                    return
                # 자식 연결선 먼저
                left_idx = 2 * index + 1
                right_idx = 2 * index + 2
                
                if left_idx < len(heap):
                    self.canvas.create_line(x, y+15, x - dx, y + 60, width=2, fill="#BDBDBD")
                    draw_node(left_idx, x - dx, y + 60, dx // 2)
                    
                if right_idx < len(heap):
                    self.canvas.create_line(x, y+15, x + dx, y + 60, width=2, fill="#BDBDBD")
                    draw_node(right_idx, x + dx, y + 60, dx // 2)

                # 노드 그리기
                bg_col = "#E3F2FD"
                out_col = "#64B5F6"
                thicc = 2
                
                if index == c_curr:
                    bg_col = "#FFF59D" # 현재 노드 노란색
                    out_col = "#FBC02D"
                    thicc = 3
                elif index == c_parent:
                    bg_col = "#C8E6C9" # 부모 노드 초록색
                    out_col = "#81C784"
                    thicc = 3
                elif index == c_sm and action == "COMPARE_DOWN":
                    bg_col = "#FFCC80" # 검색된 더 우선순위 높은 자식 주황
                    out_col = "#FF9800"
                    thicc = 3
                elif index in [c_left, c_right]:
                    bg_col = "#F5F5F5"
                    out_col = "#BDBDBD"
                
                if "SWAP" in action and index in [c_curr, c_parent, c_sm]:
                    bg_col = "#FFCDD2" # 스왑 중 빨간색 강조
                    out_col = "#EF5350"
                    
                val_text = f"{heap[index][1]}\n(p:{heap[index][0]})"
                
                self.canvas.create_oval(x - 30, y - 25, x + 30, y + 25, fill=bg_col, outline=out_col, width=thicc)
                self.canvas.create_text(x, y, text=val_text, font=("맑은 고딕", 9, "bold"), fill="#1565C0", justify=tk.CENTER)
                self.canvas.create_text(x + 35, y - 15, text=f"[{index}]", font=("Arial", 8), fill="#9E9E9E")

            draw_node(0, self.canvas_width // 2, 70, 160)

        # 2. 바텀 위쪽 영역: 힙의 배열(Array) 형태도 함께 출력
        arr_y = 350
        box_w = 60
        gap = 5
        arr_start_x = self.canvas_width // 2 - (len(heap) * (box_w + gap)) // 2
        
        self.canvas.create_text(self.canvas_width // 2, arr_y - 30, text="실제 힙 배열 (Array Representation)", font=("맑은 고딕", 11, "bold"), fill="#424242")
        
        for idx, item in enumerate(heap):
            x = arr_start_x + idx * (box_w + gap) + box_w // 2
            
            bg_col = "#FAFAFA"
            out_col = "#E0E0E0"
            thicc = 1
            
            if idx == c_curr: out_col = "#FBC02D"; thicc = 2
            elif idx == c_parent: out_col = "#81C784"; thicc = 2
            elif idx == c_sm: out_col = "#FF9800"; thicc = 2
            
            if "SWAP" in action and idx in [c_curr, c_parent, c_sm]:
                bg_col = "#FFEBEE"
                out_col = "#EF5350"
                thicc = 2

            self.canvas.create_rectangle(x - box_w//2, arr_y - 20, x + box_w//2, arr_y + 20, fill=bg_col, outline=out_col, width=thicc)
            self.canvas.create_text(x, arr_y - 5, text=f"{item[1]}", font=("맑은 고딕", 10, "bold"), fill="#424242")
            self.canvas.create_text(x, arr_y + 10, text=f"(p:{item[0]})", font=("맑은 고딕", 8), fill="#1565C0")
            self.canvas.create_text(x, arr_y + 30, text=str(idx), font=("Arial", 9), fill="#9E9E9E")
        
        # 3. 바텀 아래 영역: 처리된(Processed) 리스트
        done_start_x = 50
        done_y = 470
        self.canvas.create_text(done_start_x, done_y - 20, text="✅ 완료된 환자 (processed)", font=("맑은 고딕", 11, "bold"), fill="#212121", anchor=tk.W)
        
        for idx, item in enumerate(processed):
            x = done_start_x + 50 + idx * 80
            self.canvas.create_rectangle(x - 35, done_y - 15, x + 35, done_y + 15, 
                                         fill="#E8F5E9", outline="#81C784", width=2)
            self.canvas.create_text(x, done_y, text=item, font=("맑은 고딕", 10), fill="#388E3C")


        # 말풍선
        if reason:
            bg_color = "#424242"
            if "PUSH" in action or "UP" in action: bg_color = "#2E7D32"
            elif "POP" in action or "DOWN" in action: bg_color = "#E65100"
            elif "SWAP" in action: bg_color = "#C62828"
            
            t_id = self.canvas.create_text(self.canvas_width // 2, self.canvas_height - 30, text=reason, font=("맑은 고딕", 11, "bold"), fill="white", justify=tk.CENTER)
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
        c_job = state.get('current_job', None)
        heap = state.get('heap', [])
        
        self.lbl_heap.config(text=f"힙 배열(heap): {[f'{i[1]}({i[0]})' for i in heap]}")
        self.lbl_vars.config(text=f"현재 작업 중인 타겟: {c_job} / 총 개수: {len(heap)}")

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
            
            if action in ["PUSH_START", "POP_START"]:
                self.add_log("-----------------------------------------")
            
            self.add_log(f"{reason}")

            if not self.is_paused:
                self.status_var.set(f"[자동 진행 단계]")
            else:
                self.status_var.set(f"[일시 정지 대기중]")

            self.draw_heap_state(state, reason, action=action)
                
            current_delay = self.delay
            if action in ["FINISHED"]: 
                current_delay = int(self.delay * 2.0)
            elif "DONE" in action or "STOP" in action:
                current_delay = int(self.delay * 1.5)
            elif "SWAP" in action:
                current_delay = int(self.delay * 1.2)
            
            return current_delay
                
        except StopIteration:
            self.status_var.set("🏁 우선순위 큐 시뮬레이터 종료! 🏁")
            self.add_log("🏁 환자 관리가 모두 완료되었습니다.")
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
        if word == "heapq": desc = f"heapq: 파이썬에서 제공하는 (최소) 힙 구현 기초 모듈입니다."
        elif word == "heap": desc = f"heap: 힙 구조가 저장되는 파이썬 리스트 구조입니다. 인덱스 0이 항상 최솟값입니다."
        elif word == "heappush": desc = f"heappush(): 힙의 맨 뒤에 요소를 삽입하고 Sift-Up 을 통해 우선순위 조건을 맞춰줍니다."
        elif word == "heappop": desc = f"heappop(): 힙에서 제일 높은 우선순위 루트 노드를 꺼내고 Sift-Down 을 통해 재조정합니다."
        elif word == "processed": desc = f"processed: 순서대로 처리를 마친 리스트 결과 반환 용도입니다."

        if desc: self.tooltip.showtip(desc, event.x_root, event.y_root)
        else: self.tooltip.hidetip()
