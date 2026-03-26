import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from typing import Any

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow: Any = None
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

class HashTableVisualizer(tk.Tk):
    def __init__(self, data_pairs, search_names, generator, delay=800):
        super().__init__()
        self.title("파이썬 Dictionary 동작 (해시 테이블) 시각화")
        self.data_pairs = data_pairs
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
        
        self.lbl_hash = tk.Label(self.var_frame, text=f"키 맵핑 상태:: hash(?) = ? -> 버킷 idx (?)", font=("Consolas", 11))
        self.lbl_hash.pack(anchor=tk.W)
        self.lbl_vars = tk.Label(self.var_frame, text="현재 타겟: None", font=("Consolas", 11))
        self.lbl_vars.pack(anchor=tk.W)

        tk.Label(self.right_col, text="🖥 현재 실행 중인 코드", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W)
        self.code_text = tk.Text(self.right_col, width=54, height=13, font=("Consolas", 10), bg="#2B2B2B", fg="#A9B7C6", padx=5, pady=5)
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

    def draw_hash_state(self, state, reason, action):
        self.canvas.delete("all")
        
        buckets: list[Any] = state.get("buckets", [[] for _ in range(5)]) # type: ignore
        c_name = state.get("curr_name", None)
        c_val = state.get("curr_val", None)
        h_val = state.get("h_val", None)
        b_idx = state.get("bucket_idx", None)
        c_idx = state.get("chain_idx", None)
        
        s_name = state.get("s_name", None)
        
        res_avg = state.get("res_avg", None)
        res_top_name = state.get("res_top_name", None)
        res_top_score = state.get("res_top_score", None)
        
        # 0. 윗 공간 (Hashing Simulator)
        hash_y = 60
        self.canvas.create_text(self.canvas_width//2, 20, text="Hash Function & Mapping (사상)", font=("맑은 고딕", 11, "bold"), fill="#616161")
        
        self.canvas.create_rectangle(150, hash_y - 20, 280, hash_y + 20, fill="#E1F5FE", outline="#29B6F6", width=2)
        txt1 = "Key: ?"
        if c_name: txt1 = f"{c_name}"
        elif s_name: txt1 = f"{s_name}"
        self.canvas.create_text(215, hash_y, text=txt1, font=("Consolas", 12, "bold"))
        
        self.canvas.create_text(320, hash_y, text="   ->   \nHash()", font=("Arial", 10), fill="#757575")
        
        self.canvas.create_oval(370, hash_y - 25, 430, hash_y + 25, fill="#FFF9C4", outline="#FBC02D", width=2)
        txt2 = "?"
        if h_val is not None: txt2 = str(h_val)
        self.canvas.create_text(400, hash_y, text=txt2, font=("Consolas", 12, "bold"))

        self.canvas.create_text(480, hash_y, text="-> (% 5) ->", font=("Arial", 10), fill="#757575")

        self.canvas.create_rectangle(540, hash_y - 20, 650, hash_y + 20, fill="#E8F5E9", outline="#66BB6A", width=2)
        txt3 = "Bucket idx ?"
        if b_idx is not None: txt3 = f"Bucket: {b_idx}"
        self.canvas.create_text(595, hash_y, text=txt3, font=("Consolas", 12, "bold"), fill="#2E7D32")

        # 1. 아랫 공간 (버킷 슬롯과 체인 시각화)
        bucket_start_x = 100
        bucket_start_y = 180
        bucket_h = 280
        bucket_w = 80
        gap = 40
        self.canvas.create_text(self.canvas_width//2, bucket_start_y - 20, text="Hash Table Buckets (내부 저장소 배열)", font=("맑은 고딕", 11, "bold"), fill="#616161")
        
        for i in range(len(buckets)):
            bx = bucket_start_x + i * (bucket_w + gap)
            by = bucket_start_y
            
            # 버킷 기둥 박스 배경
            col_bg = "#F5F5F5"
            col_out = "#E0E0E0"
            if b_idx == i:
                col_bg = "#E8F5E9" if "SEARCH" in action else "#E3F2FD"
                col_out = "#81C784" if "SEARCH" in action else "#4FC3F7"
                
            self.canvas.create_rectangle(bx, by, bx + bucket_w, by + bucket_h, fill=col_bg, outline=col_out, width=2)
            self.canvas.create_text(bx + bucket_w//2, by - 10, text=f"[{i}]", font=("Consolas", 12, "bold"))

            # 버킷 내부의 Key-Value 노드들
            for j, (k, v) in enumerate(buckets[i]): # type: ignore
                nx = bx + bucket_w//2
                ny = by + 30 + j * 50
                
                n_bg = "#FFFFFF"
                n_out = "#BDBDBD"
                n_thicc = 1
                
                # 방금 삽입되었으면 파란색 테두리 подчер기
                if "INSERT_DONE" in action and b_idx == i and j == len(buckets[i])-1: # type: ignore
                    n_bg = "#BBDEFB"; n_out = "#1976D2"; n_thicc = 3
                
                if "SEARCH_CHAIN" in action and b_idx == i and c_idx == j:
                    n_bg = "#FFF9C4"; n_out = "#FBC02D"; n_thicc = 3
                if "SEARCH_FOUND" in action and b_idx == i and c_idx == j:
                    n_bg = "#C8E6C9"; n_out = "#388E3C"; n_thicc = 3

                self.canvas.create_rectangle(nx - 35, ny - 20, nx + 35, ny + 20, fill=n_bg, outline=n_out, width=n_thicc)
                self.canvas.create_text(nx, ny - 6, text=f"{k}", font=("맑은 고딕", 10, "bold"), fill="#212121")
                self.canvas.create_text(nx, ny + 8, text=f": {v}", font=("Arial", 9), fill="#1565C0")

        # 2. 결과 출력 공간
        if res_avg is not None:
            self.canvas.create_rectangle(50, 480, 750, 520, fill="#FFFDE7", outline="#FBC02D")
            self.canvas.create_text(400, 500, text=f"평균 점수: {res_avg:.1f} | 최고 점수 학생: '{res_top_name}' ({res_top_score}점) ", font=("맑은 고딕", 11, "bold"), fill="#F57C00")

        # 말풍선
        if reason:
            bg_color = "#424242"
            if "HASH" in action or "MOD" in action: bg_color = "#9C27B0"
            elif "COLL" in action or "NOT_FOUND" in action: bg_color = "#D32F2F"
            elif "DONE" in action or "FOUND" in action: bg_color = "#2E7D32"
            elif "CALC" in action: bg_color = "#1565C0"
            elif "SEARCH" in action: bg_color = "#E65100"
            
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
        c_name = state.get("curr_name", None)
        s_name = state.get("s_name", None)
        h_val = state.get("h_val", "?")
        b_idx = state.get("bucket_idx", "?")
        target = c_name if c_name else (s_name if s_name else "None")
        
        self.lbl_hash.config(text=f"키 맵핑 상태:: hash('{target}') = {h_val} -> 버킷 idx ({b_idx})")
        
        # 잔여 변수 표시
        extra_str = ""
        c_val = state.get("curr_val", None)
        if c_val is not None: extra_str = f" / 삽입할 값: {c_val}"
        self.lbl_vars.config(text=f"현재 타겟: {target}{extra_str}")

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
            self.after(delay_used, lambda: self.auto_step()) # type: ignore

    def execute_single_step(self):
        if not self.winfo_exists(): return None
        try:
            val = next(self.generator)
            action = str(val[0])
            state = val[1]
            code_line = val[2]
            reason = str(val[3])

            self.current_vars = state
            self.highlight_code_line(code_line)
            self.update_vars(state)
            
            if action in ["INSERT_START", "SEARCH_START", "SETUP_DONE"]:
                self.add_log("-----------------------------------------")
            
            self.add_log(f"{reason}")

            if not self.is_paused:
                self.status_var.set(f"[자동 진행 단계]")
            else:
                self.status_var.set(f"[일시 정지 대기중]")

            self.draw_hash_state(state, reason, action=action)
                
            current_delay = self.delay
            if action in ["FINISHED", "SETUP_DONE", "RETURN_MGMT"]: 
                current_delay = int(self.delay * 2.5)
            elif "CALC" in action or "DONE" in action or "FOUND" in action:
                current_delay = int(self.delay * 1.5)
            elif "HASH" in action or "MOD" in action:
                current_delay = int(self.delay * 0.8)
            
            return current_delay
                
        except StopIteration:
            self.status_var.set("🏁 해시 테이블 동작 시뮬레이션 종료! 🏁")
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
        
        desc = ""
        if word == "students": desc = f"students: 내부적으로 해시 테이블로 동작하는 파이썬 딕셔너리 모의 객체입니다."
        elif word == "average": desc = f"average: 딕셔너리의 모든 value를 순회하여 평균을 낸 변수입니다."
        elif word == "max": desc = f"max(dict, key=dict.get): 성적이 가장 높은 key(학생)를 순회 탐색합니다."
        elif word == "name": desc = f"name in students: O(1) 해시 룩업을 통해 학생이 딕셔너리에 존재하는 지 조회합니다."

        if desc: self.tooltip.showtip(desc, event.x_root, event.y_root)
        else: self.tooltip.hidetip()
