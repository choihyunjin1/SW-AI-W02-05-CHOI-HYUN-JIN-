import tkinter as tk
from tkinter import messagebox

class DivConqVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("분할 정복 (거듭제곱) 알고리즘 시각화 학습 도구")
        self.geometry("900x700")
        self.configure(bg="#f0f0f0")
        
        # 초기 변수 셋업
        self.A = 0
        self.B = 0
        self.C = 0
        
        self.history = []
        self.step_idx = 0
        self.active_calls = [] # 화면에 그릴 활성 호출 목록
        self.call_returns = {} # 깊이별 반환값 저장
        self.current_focus_depth = 0 # 현재 연산이 이루어지는 깊이
        
        self.setup_ui()
        
    def setup_ui(self):
        # 상단 컨트롤 패널
        control_frame = tk.Frame(self, bg="#e0e0e0", pady=13)
        control_frame.pack(fill=tk.X, side=tk.TOP)
        
        tk.Label(control_frame, text="A, B, C 입력 (공백 구분):", bg="#e0e0e0", font=("맑은 고딕", 12)).pack(side=tk.LEFT, padx=10)
        
        self.input_entry = tk.Entry(control_frame, width=20, font=("Arial", 12))
        self.input_entry.insert(0, "10 11 12")
        self.input_entry.pack(side=tk.LEFT, padx=10)
        
        self.btn_load = tk.Button(control_frame, text="불러오기", font=("맑은 고딕", 11, "bold"), command=self.load_data)
        self.btn_load.pack(side=tk.LEFT, padx=5)
        
        self.btn_step = tk.Button(control_frame, text="다음 단계 (Step)", font=("맑은 고딕", 11, "bold"), command=self.step, state=tk.DISABLED, bg="#d4edda")
        self.btn_step.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(control_frame, text="초기화", font=("맑은 고딕", 11, "bold"), command=self.reset)
        self.btn_reset.pack(side=tk.LEFT, padx=5)
        
        # 메인 캔버스 (재귀 흐름 스택 그리기)
        self.canvas_frame = tk.Frame(self, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 스크롤바 추가
        self.vbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", yscrollcommand=self.vbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vbar.config(command=self.canvas.yview)
        
        # 하단 상태 정보 패널
        info_frame = tk.Frame(self, bg="#f8f9fa", pady=15)
        info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.lbl_status = tk.Label(info_frame, text="데이터를 불러와주세요. (A B C 입력 후 불러오기 클릭)", font=("맑은 고딕", 13, "bold"), bg="#f8f9fa", fg="#333333")
        self.lbl_status.pack(pady=5)
        
        self.lbl_expr = tk.Label(info_frame, text="", font=("Courier New", 14, "bold"), bg="#f8f9fa", fg="blue")
        self.lbl_expr.pack(pady=2)

    def load_data(self):
        raw_text = self.input_entry.get().strip()
        try:
            parts = raw_text.split()
            if len(parts) != 3:
                raise ValueError
            self.A, self.B, self.C = map(int, parts)
            if self.B < 1 or self.C < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("입력 오류", "A, B, C 세 개의 양의 정수를 공백으로 구분하여 입력해주세요.")
            return

        self.reset_state()
        self.generate_history(self.A, self.B, self.C)
        self.btn_step.config(state=tk.NORMAL)
        self.lbl_status.config(text=f"데이터 로드 완료! solve({self.A}, {self.B}, {self.C}) 실행을 시작합니다. '다음 단계'를 눌러주세요.")
        self.lbl_expr.config(text="")
        
    def reset_state(self):
        self.history = []
        self.step_idx = 0
        self.active_calls = []
        self.call_returns = {}
        self.current_focus_depth = 0
        self.canvas.delete("all")
        self.canvas.yview_moveto(0)
        
    def reset(self):
        self.reset_state()
        self.btn_step.config(state=tk.DISABLED)
        self.lbl_status.config(text="데이터를 불러와주세요. (A B C 입력 후 불러오기 클릭)")
        self.lbl_expr.config(text="")

    def generate_history(self, a, b, c):
        # 시뮬레이션을 통해 모든 실행 이력을 배열에 기록
        def simulate(cur_a, cur_b, cur_c, depth=0):
            # 호출 이벤트 추가
            self.history.append({"type": "CALL", "a": cur_a, "b": cur_b, "c": cur_c, "depth": depth})
            
            # 기저 조건 (종료 조건)
            if cur_b == 1:
                res = cur_a % cur_c
                self.history.append({"type": "BASE", "res": res, "depth": depth, "b": cur_b, "a": cur_a, "c": cur_c})
                return res
            
            # 분할 단계
            self.history.append({"type": "DIVIDE", "b": cur_b, "next_b": cur_b // 2, "depth": depth})
            temp = simulate(cur_a, cur_b // 2, cur_c, depth + 1)
            
            # 병합 단계 (부분해를 이용해 현재 문제 해결 기능)
            if cur_b % 2 == 0:
                res = (temp * temp) % cur_c
                self.history.append({"type": "RETURN_EVEN", "temp": temp, "res": res, "depth": depth, "b": cur_b, "a": cur_a, "c": cur_c})
                return res
            else:
                res = (temp * temp * cur_a) % cur_c
                self.history.append({"type": "RETURN_ODD", "temp": temp, "res": res, "depth": depth, "b": cur_b, "a": cur_a, "c": cur_c})
                return res

        simulate(a, b, c)

    def draw_state(self):
        self.canvas.delete("all")
        
        self.update_idletasks() # 너비 측정을 위해 업데이트
        c_width = self.canvas.winfo_width()
        if c_width <= 1: c_width = 850
        
        card_w = 320
        card_h = 80
        spacing_y = 45
        
        start_x = c_width // 2
        start_y = 50
        
        max_y = 0 # 스크롤 영역 제한 계산
        
        # 깊이별 카드 기준 위치(중심 좌표) 반환 함수
        def get_coords(d):
            return start_x, start_y + d * (card_h + spacing_y)
        
        for i, call in enumerate(self.active_calls):
            depth = call['depth']
            cx, cy = get_coords(depth)
            
            x0 = cx - card_w//2
            y0 = cy
            x1 = cx + card_w//2
            y1 = cy + card_h
            
            max_y = max(max_y, y1 + spacing_y)
            
            # 이전 함수 호출로부터 내려오는 연결선 화살표
            if i > 0:
                pcx, pcy = get_coords(self.active_calls[i-1]['depth'])
                self.canvas.create_line(pcx, pcy + card_h, cx, y0, arrow=tk.LAST, fill="#a0a0a0", width=2)
            
            # 진행 상태에 따른 카드 테마 색상 설정
            bg_color = "#e1f5fe" # 기본 진행 시에는 맑은 파랑
            if depth == self.current_focus_depth:
                bg_color = "#fff9c4" # 현재 진행 중인 노드는 노란색 강조
            if depth in self.call_returns:
                bg_color = "#c8e6c9" # 연산이 끝난(리턴된) 노드는 녹색 표시
                
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color, outline="#4fc3f7", width=2)
            
            # 카드 내 함수 호출 시그니처 표기
            func_text = f"solve({call['a']}, {call['b']}, {call['c']})"
            self.canvas.create_text(cx, cy + 20, text=func_text, font=("Courier New", 14, "bold"))
            
            # 반환값 또는 대기 상태 메세지 표기
            if depth in self.call_returns:
                ret_val = self.call_returns[depth]
                self.canvas.create_text(cx, cy + 50, text=f"반환(Return): {ret_val}", font=("맑은 고딕", 12, "bold"), fill="#d32f2f")
                
                # 자식 노드에서 값이 반환되어 올라오는 경우 화살표 표현 (우측선)
                if i < len(self.active_calls) - 1:
                    child_depth = self.active_calls[i+1]['depth']
                    ccx, ccy = get_coords(child_depth)
                    if child_depth in self.call_returns:
                        # 자식에서 부모로 전해지는 화살표 (오른쪽으로 살짝 이동)
                        offset = card_w//2 - 25
                        self.canvas.create_line(cx + offset, ccy, cx + offset, y1, arrow=tk.LAST, fill="#d32f2f", width=2, dash=(4,2))
            else:
                self.canvas.create_text(cx, cy + 50, text="하위 문제 해결(temp) 대기 중...", font=("맑은 고딕", 11), fill="#757575")

        # 캔버스 스크롤 가능 영역 업데이트
        self.canvas.config(scrollregion=(0, 0, c_width, max_y))
        
        # 현재 활성화된 카드가 화면 중앙에 위치하도록 스크롤 이동
        if len(self.active_calls) > 0:
            focus_y = get_coords(self.current_focus_depth)[1]
            canvas_h = self.canvas.winfo_height()
            if focus_y > canvas_h / 2:
                fraction = (focus_y - canvas_h / 2) / max_y
                self.canvas.yview_moveto(fraction)

    def step(self):
        if self.step_idx >= len(self.history):
            self.lbl_status.config(text="시각화가 모두 완료되었습니다!")
            self.lbl_expr.config(text="")
            self.btn_step.config(state=tk.DISABLED)
            return
            
        event = self.history[self.step_idx]
        self.current_focus_depth = event['depth']
        
        if event['type'] == 'CALL':
            # 새로운 함수 호출을 그리기 위한 리스트 편입
            self.active_calls.append(event)
            self.lbl_status.config(text=f"⬇️ [재귀 호출] 문제를 쪼개기 위해 solve({event['a']}, {event['b']}, {event['c']}) 함수를 호출합니다.")
            self.lbl_expr.config(text="")
            
        elif event['type'] == 'BASE':
            # 종료 조건 도달
            self.call_returns[event['depth']] = event['res']
            self.lbl_status.config(text=f"✅ [기저 조건] b가 1이 되었습니다! 즉시 모듈러 연산을 수행해 계산을 마칩니다.")
            self.lbl_expr.config(text=f"return {event['a']} % {event['c']}  =>  {event['res']}")
            
        elif event['type'] == 'DIVIDE':
            # 분할 및 변수 설명
            self.lbl_status.config(text=f"✂️ [분할] 큰 지수 b({event['b']})를 반으로 나눕니다. 더 작은 문제인 (b={event['next_b']})를 재귀호출합니다.")
            self.lbl_expr.config(text=f"temp = solve({self.A}, {event['next_b']}, {self.C})")
            
        elif event['type'] == 'RETURN_EVEN':
            # 짝수일 때 값 병합(합치기)
            self.call_returns[event['depth']] = event['res']
            self.lbl_status.config(text=f"⬆️ [병합 - 짝수] b={event['b']}은(는) 짝수입니다. 하위에서 반환받은 temp({event['temp']})를 제곱합니다.")
            self.lbl_expr.config(text=f"return ({event['temp']} * {event['temp']}) % {event['c']}  =>  {event['res']}")

        elif event['type'] == 'RETURN_ODD':
            # 홀수일 때 값 병합
            self.call_returns[event['depth']] = event['res']
            self.lbl_status.config(text=f"⬆️ [병합 - 홀수] b={event['b']}은(는) 홀수입니다. temp({event['temp']}) 제곱에 {event['a']}를 하나 더 곱해줍니다.")
            self.lbl_expr.config(text=f"return ({event['temp']} * {event['temp']} * {event['a']}) % {event['c']}  =>  {event['res']}")

        # 시각적 반영 수행
        self.draw_state()
        self.step_idx += 1
        
        # 마지막 스텝까지 도달했을 시 완료 알림
        if self.step_idx >= len(self.history):
            self.lbl_status.config(text=f"🏁 [최종 완료] 정답: {self.call_returns[0]} (계산이 모두 끝났습니다!)")
            self.btn_step.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = DivConqVisualizer()
    app.mainloop()
