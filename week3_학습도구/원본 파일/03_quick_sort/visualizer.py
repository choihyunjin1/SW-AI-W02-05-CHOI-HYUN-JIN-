# visualizer.py
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
        self.tipwindow.wm_overrideredirect(1) # type: ignore
        self.tipwindow.wm_geometry(f"+{x + 15}+{y + 15}") # type: ignore
        
        label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("맑은 고딕", 10), padx=5, pady=3)
        label.pack()

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy() # type: ignore
            self.tipwindow = None

class QuickSortVisualizer(tk.Tk):
    def __init__(self, arr, generator, delay=350):
        super().__init__()
        self.title("퀵 정렬(Quick Sort) 알고리즘 학습 도구")
        self.n = len(arr)
        self.max_val = max(arr) if arr else 1
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
        
        # ===== [좌측 영역: 배열 시각화 캔버스] =====
        self.canvas_width = 800
        self.canvas_height = 450
        self.canvas = tk.Canvas(self.left_col, width=self.canvas_width, height=self.canvas_height, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.canvas.pack(pady=5)
        
        self.status_var = tk.StringVar(value="초기화 중...")
        tk.Label(self.left_col, textvariable=self.status_var, font=("맑은 고딕", 12, "bold"), fg="blue").pack(pady=5)

        # 변수 상태 뷰
        self.var_frame = tk.LabelFrame(self.left_col, text="💡 현재 변수 상태(State Monitor)", font=("맑은 고딕", 11, "bold"), fg="#D32F2F")
        self.var_frame.pack(fill=tk.X, pady=5, ipadx=5, ipady=5)
        
        self.lbl_pointers = tk.Label(self.var_frame, text="low: ? / high: ? / i: ? / j: ?", font=("Consolas", 11))
        self.lbl_pointers.pack(anchor=tk.W)
        self.lbl_vars = tk.Label(self.var_frame, text="pibut: ? / p: ?", font=("Consolas", 11))
        self.lbl_vars.pack(anchor=tk.W)

        # ===== [우측 영역: 코드 패널과 히스토리 로그 패널] =====
        tk.Label(self.right_col, text="🖥 현재 실행 중인 코드", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W)
        self.code_text = tk.Text(self.right_col, width=54, height=26, font=("Consolas", 10), bg="#2B2B2B", fg="#A9B7C6", padx=5, pady=5)
        self.code_text.pack(fill=tk.X)
        self.code_text.tag_config("highlight", background="#4B4D4D", foreground="#FFFFFF", font=("Consolas", 10, "bold"))
        self.code_text.config(state=tk.DISABLED) 
        
        self.tooltip = ToolTip(self.code_text)
        self.code_text.bind("<Motion>", self.on_code_hover)
        self.code_text.bind("<Leave>", lambda e: self.tooltip.hidetip())
        self.current_vars = {}

        tk.Label(self.right_col, text="📜 스텝 실행 로그", font=("맑은 고딕", 12, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.log_text = ScrolledText(self.right_col, width=54, height=10, font=("맑은 고딕", 10), bg="#F5F5F5")
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

        self.code_lines = []
        
        try:
            action, code_source, _, msg = next(self.generator)
            if action == "INIT_CODE":
                self.init_code_view(code_source)
                self.draw_arrays(arr, -1, -1, -1, -1, None, -1, msg)
        except StopIteration:
            pass

    def add_log(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def draw_arrays(self, arr, low, high, i, j, pibut, p, reason, action=""):
        self.canvas.delete("all")
        if not arr: return
        
        # 막대 넓이 및 간격
        max_bars_w = min(50, (self.canvas_width - 40 - (self.n - 1) * 8) // self.n)
        bx_w = max_bars_w
        gap = 8
        total_w = self.n * bx_w + (self.n - 1) * gap
        start_x = (self.canvas_width - total_w) // 2
        
        max_h = 240
        y_base = max_h + 80
        
        # 1. 파티션 범위(low~high) 배경 상자 (시각적 분리)
        if low != -1 and high != -1:
            rx1 = start_x + low * (bx_w + gap) - gap//2
            rx2 = start_x + high * (bx_w + gap) + bx_w + gap//2
            self.canvas.create_rectangle(rx1, 20, rx2, y_base + 60, fill="#f0ebf8", outline="#cbbaf0", dash=(4, 4))
            self.canvas.create_text((rx1+rx2)/2, 35, text=f"현재 분할 범위 (low={low} ~ high={high})", font=("맑은 고딕", 11, "bold"), fill="#673ab7")
        
        for idx in range(self.n):
            val = arr[idx]
            x1 = start_x + idx * (bx_w + gap)
            
            # 높이 계산 (최대값 대비 비율)
            h = max(20, int((val / self.max_val) * max_h)) if self.max_val > 0 else 20
            y1 = y_base - h
            x2 = x1 + bx_w
            y2 = y_base
            
            # 테두리와 배경색
            bg_col = "#E0E0E0" # 기본 회색
            outline_col = "#757575"
            thicc = 1
            
            # 포인터가 가리키는 것에 따른 색상 처리
            if idx == j:
                bg_col = "#FFF59D" # 노란색 (현재 순회)
                outline_col = "#FBC02D"
                thicc = 2
            elif idx == i:
                bg_col = "#81D4FA" # 하늘색 (작은 원소들의 마지노선)
                outline_col = "#0288D1"
                thicc = 2
                
            if idx == high and high != -1:
                bg_col = "#FFCDD2" # 빨간색 (피벗)
                outline_col = "#D32F2F"
                thicc = 2
                
            if idx == p and p != -1: # 정렬 완료된 제자리 피벗
                bg_col = "#C8E6C9" # 초록색
                outline_col = "#388E3C"
                thicc = 3
                
            # 막 교환(SWAP)이 일어나는 경우
            if "SWAP" in action and idx in (i, j) and idx != -1:
                bg_col = "#CE93D8" # 보라색 강조
                outline_col = "#6A1B9A"
                thicc = 3
                
            # 피벗이 최종 위치로 배치되는 경우
            if "PLACE_PIVOT" in action and idx in (high, i+1) and idx != -1:
                bg_col = "#FFCC80" # 주황색 강조
                outline_col = "#E65100"
                thicc = 3
                
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_col, outline=outline_col, width=thicc)
            # 값 텍스트
            self.canvas.create_text((x1+x2)/2, y1 - 12, text=str(val), font=("Consolas", 12, "bold"))
            # 인덱스 텍스트
            self.canvas.create_text((x1+x2)/2, y2 + 15, text=f"[{idx}]", font=("Arial", 9))
            
            # 포인터 텍스트 라벨 추가 (i, j, pivot 화살표 느낌)
            pointers = []
            if idx == i: pointers.append("i")
            if idx == j: pointers.append("j")
            if idx == high: pointers.append("pivot")
            if idx == p: pointers.append("p")
            
            if pointers:
                p_text = "\n".join(pointers)
                self.canvas.create_text((x1+x2)/2, y2 + 35, text=p_text, font=("Consolas", 11, "bold"), fill="#1565C0")

        # 2. 말풍선(reason) 박스 시각화
        if reason:
            bg_color = "#424242"
            if "SWAP" in action: bg_color = "#6A1B9A"
            elif "COMPARE" in action: bg_color = "#E65100"
            elif "PLACE" in action: bg_color = "#D84315"
            elif "FINISH" in action: bg_color = "#2E7D32"
            elif action in ["FUNC_CALL", "RETURN", "CALL_PARTITION"]: bg_color = "#0277BD"
            
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
        low = state.get('low', -1)
        high = state.get('high', -1)
        i = state.get('i', -1)
        j = state.get('j', -1)
        pibut = state.get('pibut', None)
        p = state.get('p', -1)
        
        self.lbl_pointers.config(text=f"범위: low={low if low!=-1 else '?'} ~ high={high if high!=-1 else '?'}, 인덱스: i={i if i!=-1 else '?'}, j={j if j!=-1 else '?'}")
        self.lbl_vars.config(text=f"현재 피벗 값 pibut: {pibut if pibut is not None else '?'}, 변환된 피벗 인덱스 p: {p if p!=-1 else '?'}")

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
            action, state, code_line, reason = next(self.generator)

            self.current_vars = state
            self.highlight_code_line(code_line)
            self.update_vars(state)
            
            if action in ["FUNC_CALL", "RETURN", "CALL_PARTITION", "PARTITION_CALL"]:
                self.add_log("-----------------------------------------")
            log_txt = f"{reason}"
            self.add_log(log_txt)

            if not self.is_paused:
                self.status_var.set(f"[자동 진행 단계]")
            else:
                self.status_var.set(f"[일시 정지 대기중]")

            self.draw_arrays(
                state.get("arr", []), 
                state.get("low", -1), 
                state.get("high", -1), 
                state.get("i", -1), 
                state.get("j", -1), 
                state.get("pibut", None), 
                state.get("p", -1), 
                reason, 
                action=action
            )
                
            current_delay = self.delay
            if "SWAP" in action or "PLACE_PIVOT" in action: 
                current_delay = int(self.delay * 1.5)
            elif "COMPARE" in action:
                current_delay = int(self.delay * 0.8)
            elif "LOOP_J" in action:
                current_delay = int(self.delay * 0.5)
            
            return current_delay
                
        except StopIteration:
            self.status_var.set("🏁 탐색 완료! 모든 정렬이 끝났습니다. 🏁")
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
        if word == "arr": desc = f"arr (현재 배열 원소)\n{cv.get('arr', '?')}"
        elif word == "low": desc = f"low (시작 인덱스) = {cv.get('low', '?')}"
        elif word == "high": desc = f"high (끝 인덱스, 주로 피벗으로 사용) = {cv.get('high', '?')}"
        elif word == "pibut": desc = f"pibut (피벗, 기준값) = {cv.get('pibut', '?')}"
        elif word == "i": desc = f"i (피벗보다 작은 원소의 마지막 위치) = {cv.get('i', '?')}"
        elif word == "j": desc = f"j (현재 비교 중인 원소 위치) = {cv.get('j', '?')}"
        elif word == "p": desc = f"p (새롭게 찾은 피벗의 정확한 위치 인덱스) = {cv.get('p', '?')}"
        elif word == "partition": desc = "partition 함수: 피벗을 기준으로 작은 값은 왼쪽, 큰 값은 오른쪽으로 재배치"
        elif word == "quick_sort_helper": desc = "quick_sort_helper 함수: 실질적인 재귀 호출 함수 (Divide & Conquer)"

        if desc: self.tooltip.showtip(desc, event.x_root, event.y_root)
        else: self.tooltip.hidetip()
