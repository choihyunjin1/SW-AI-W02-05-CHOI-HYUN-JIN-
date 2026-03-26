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

class LinkedListVisualizer(tk.Tk):
    def __init__(self, values, generator, delay=800):
        super().__init__()
        self.title("단순 연결 리스트 (Singly Linked List) 구조 시각화")
        self.values = values
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
        
        self.lbl_head = tk.Label(self.var_frame, text=f"연결 리스트 시작점(head): None", font=("Consolas", 11))
        self.lbl_head.pack(anchor=tk.W)
        self.lbl_vars = tk.Label(self.var_frame, text="현재 탐색 포인터(current): None", font=("Consolas", 11))
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


    def draw_list_state(self, state, reason, action):
        self.canvas.delete("all")
        
        nodes = state.get("nodes", [])
        head_id = state.get("head_id", None)
        new_node_id = state.get("new_node_id", None)
        curr_ptr_id = state.get("curr_ptr_id", None)
        
        head_changing = state.get("head_ptr_changing", False)
        link_changing_source = state.get("link_changing", None)
        res_values = state.get("res_values", None)
        
        # 0. 메모리 공간 캔버스 배경 스케치
        self.canvas.create_text(20, 20, text="메모리 힙 (Memory Heap) 상의 Node 객체들", font=("맑은 고딕", 11, "bold"), fill="#9E9E9E", anchor=tk.W)
        
        # 노드들을 렌더링하기 위한 위치 계산
        # 연결 리스트 특성상 메모리상 흩어져 있을 수 있으나 알아보기 쉽게 일렬 렌더링
        node_positions = {} # { "id": (x, y) }
        start_x = 100
        start_y = 250
        gap_x = 150
        
        for i, node in enumerate(nodes):
            nid = node["id"]
            if nid == new_node_id and ("CREATE" in action or "CHECK" in action):
                # 방금 생성되어 아직 연결 전인 노드는 위쪽에 붕 띄워서 표시
                node_positions[nid] = (start_x + i * gap_x, 100)
            else:
                node_positions[nid] = (start_x + i * gap_x, start_y)
                
        # 1. 노드 간의 화살표 연결선 (next 포인터) 렌더링
        for node in nodes:
            nid = node["id"]
            nxt_id = node.get("next_id")
            
            if nid in node_positions and nxt_id in node_positions:
                x1, y1 = node_positions[nid]
                x2, y2 = node_positions[nxt_id]
                
                # 방금 연결 링크가 생성된거면 주황색 강조
                line_col = "#616161"
                thicc = 3
                dash = None
                
                if link_changing_source == nid and action == "APPEND_DONE_LINK":
                    line_col = "#FF9800"
                    thicc = 4
                    dash = (4,2)
                    
                # 노드 박스 우측에서 다음 박스 좌측으로
                # 박스 절반 크기 보정 (아래 노드 그릴때 박스 폭 W=80) 
                
                self.canvas.create_line(x1 + 40, y1, x2 - 40, y2, arrow=tk.LAST, width=thicc, fill=line_col, dash=dash)

        # 2. 노드 박스 그리기
        for node in nodes:
            nid = node["id"]
            if nid not in node_positions: continue
            
            x, y = node_positions[nid]
            val = node["data"]
            
            # 박스
            bg_col = "#E3F2FD"
            out_col = "#64B5F6"
            thicc = 2
            
            if "CREATE" in action and nid == new_node_id:
                bg_col = "#DCEDC8"; out_col = "#8BC34A"; thicc = 3
            elif curr_ptr_id == nid:
                # current 포인터가 가리키고 있음
                bg_col = "#FFF9C4"; out_col = "#FBC02D"; thicc = 3

            # 데이터 구역과 참조(next) 구역을 반으로 나눠서 그리는 클래식한 방식 표현
            box_w = 80
            box_h = 40
            # 전체 바깥
            self.canvas.create_rectangle(x - box_w//2, y - box_h//2, x + box_w//2, y + box_h//2, fill=bg_col, outline=out_col, width=thicc)
            # 중간 칸막이
            self.canvas.create_line(x, y - box_h//2, x, y + box_h//2, fill=out_col, width=thicc)
            # 글씨
            self.canvas.create_text(x - box_w//4, y, text=str(val), font=("Consolas", 14, "bold"), fill="#333333")
            
            out_ptr = "● " if node["next_id"] else "None"
            self.canvas.create_text(x + box_w//4, y, text=out_ptr, font=("Consolas", 10), fill="#757575")
            
            # 주소 식별자 표기
            self.canvas.create_text(x, y + box_h//2 + 15, text=f"addr:{nid}", font=("Arial", 8), fill="#9E9E9E")

        # 3. Head 포인터 가리키미
        head_x, head_y = 50, 450
        self.canvas.create_rectangle(head_x - 30, head_y - 20, head_x + 30, head_y + 20, fill="#F5F5F5", outline="#BDBDBD", width=2)
        self.canvas.create_text(head_x, head_y, text="HEAD", font=("맑은 고딕", 12, "bold"), fill="#D32F2F")
        
        if head_id and head_id in node_positions:
            nx, ny = node_positions[head_id]
            h_col = "#D32F2F"
            h_thicc = 3
            dash = None
            if head_changing:
                h_col = "#FF9800"
                h_thicc = 4
                dash = (4,2)
                
            self.canvas.create_line(head_x, head_y - 20, head_x, head_y - 80, nx - 40, ny, arrow=tk.LAST, width=h_thicc, fill=h_col, dash=dash)
        else:
             self.canvas.create_text(head_x + 60, head_y, text="-> None", font=("Consolas", 11, "bold"), fill="#9E9E9E")

        # 4. Current 포인터 가리키미
        curr_x, curr_y = 150, 450
        self.canvas.create_rectangle(curr_x - 40, curr_y - 20, curr_x + 40, curr_y + 20, fill="#FFFDE7", outline="#FBC02D", width=2)
        self.canvas.create_text(curr_x, curr_y, text="CURRENT", font=("맑은 고딕", 11, "bold"), fill="#F57C00")

        if curr_ptr_id and curr_ptr_id in node_positions:
            cx, cy = node_positions[curr_ptr_id]
            self.canvas.create_line(curr_x, curr_y - 20, curr_x, curr_y - 50, cx, cy + 20, arrow=tk.LAST, width=3, fill="#F57C00")
        else:
            self.canvas.create_text(curr_x + 70, curr_y, text="-> ? (None)", font=("Consolas", 11), fill="#9E9E9E")

        # 5. 출력 배열 상태 (PRINT 페이즈시 등장)
        if res_values is not None:
            res_y = 100
            res_str = "[" + ", ".join(map(str, res_values)) + "]"
            self.canvas.create_text(self.canvas_width - 150, res_y - 20, text="출력 수집 배열 (values)", font=("맑은 고딕", 11, "bold"), fill="#424242")
            self.canvas.create_rectangle(self.canvas_width - 250, res_y, self.canvas_width - 50, res_y + 40, fill="#E8F5E9", outline="#81C784", width=2)
            self.canvas.create_text(self.canvas_width - 150, res_y + 20, text=res_str, font=("Consolas", 12, "bold"), fill="#388E3C")


        # 말풍선
        if reason:
            bg_color = "#424242"
            if "CREATE" in action or "SET" in action: bg_color = "#2E7D32"
            elif "MOVE" in action or "CHECK" in action: bg_color = "#E65100"
            elif "PRINT" in action: bg_color = "#0277BD"
            elif "ERROR" in action or "FAIL" in action: bg_color = "#D32F2F"
            
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
        head = state.get('head_id', None)
        curr = state.get('curr_ptr_id', None)
        
        self.lbl_head.config(text=f"연결 리스트 시작점(head): {head if head else 'None'}")
        self.lbl_vars.config(text=f"현재 탐색 포인터(current): {curr if curr else 'None'}")

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
            
            if action in ["APPEND_CALL", "PRINT_CALL"]:
                self.add_log("-----------------------------------------")
            
            self.add_log(f"{reason}")

            if not self.is_paused:
                self.status_var.set(f"[자동 진행 단계]")
            else:
                self.status_var.set(f"[일시 정지 대기중]")

            self.draw_list_state(state, reason, action=action)
                
            current_delay = self.delay
            if action in ["FINISHED", "APPEND_ALL_DONE"]: 
                current_delay = int(self.delay * 2.5)
            elif "DONE" in action or "SET" in action or "CALL" in action:
                current_delay = int(self.delay * 1.5)
            elif "CHECK" in action:
                current_delay = int(self.delay * 0.8)
            
            return current_delay
                
        except StopIteration:
            self.status_var.set("🏁 연결 리스트 시각화 동작 검증 완료! 🏁")
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
        if word == "Node": desc = f"Node: 데이터와 다음 주소를 담을 수 있는 연결 리스트의 기본 구조체 조각입니다."
        elif word == "head": desc = f"head: 연결이 시작되는 가장 첫번째 머리 노드의 주소를 기억하는 변수입니다."
        elif word == "next": desc = f"next: 각 노드가 손에 쥐고 있는 포인터로, 다음 노드의 메모리 주소를 가리킵니다."
        elif word == "current": desc = f"current: 리스트를 끝까지 탐색하기 위해 옮겨 다니는 주소 보관용 (iterator) 변수입니다."

        if desc: self.tooltip.showtip(desc, event.x_root, event.y_root)
        else: self.tooltip.hidetip()
