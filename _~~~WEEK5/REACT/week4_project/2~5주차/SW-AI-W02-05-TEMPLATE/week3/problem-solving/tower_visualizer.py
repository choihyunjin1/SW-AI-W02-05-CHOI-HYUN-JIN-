import tkinter as tk
from tkinter import messagebox

class TowerVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("탑(Top) 알고리즘 시각화 학습 도구")
        self.geometry("900x650")
        self.configure(bg="#f0f0f0")
        
        # 데이터 초기화
        self.heights = []
        self.stack = []    # (탑 번호, 높이)
        self.answer = []
        self.current_idx = 0
        self.laser_animating = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # 상단 컨트롤 패널
        control_frame = tk.Frame(self, bg="#e0e0e0", pady=10)
        control_frame.pack(fill=tk.X, side=tk.TOP)
        
        tk.Label(control_frame, text="탑 높이 입력 (공백 구분):", bg="#e0e0e0", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        
        self.input_entry = tk.Entry(control_frame, width=40, font=("Arial", 12))
        self.input_entry.insert(0, "6 9 5 7 4")
        self.input_entry.pack(side=tk.LEFT, padx=10)
        
        self.btn_load = tk.Button(control_frame, text="불러오기", font=("Arial", 11, "bold"), command=self.load_data)
        self.btn_load.pack(side=tk.LEFT, padx=5)
        
        self.btn_step = tk.Button(control_frame, text="다음 단계 (Step)", font=("Arial", 11, "bold"), command=self.step, state=tk.DISABLED, bg="#d4edda")
        self.btn_step.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(control_frame, text="초기화", font=("Arial", 11, "bold"), command=self.reset)
        self.btn_reset.pack(side=tk.LEFT, padx=5)
        
        # 메인 캔버스 (탑 그리기)
        self.canvas_frame = tk.Frame(self, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 하단 상태 정보 패널
        info_frame = tk.Frame(self, bg="#f8f9fa", pady=10)
        info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.lbl_status = tk.Label(info_frame, text="데이터를 불러와주세요.", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#333333")
        self.lbl_status.pack(pady=5)
        
        self.lbl_stack = tk.Label(info_frame, text="스택 상태: []", font=("Arial", 12), bg="#f8f9fa", fg="blue")
        self.lbl_stack.pack(pady=2)
        
        self.lbl_answer = tk.Label(info_frame, text="수신 결과: []", font=("Arial", 12), bg="#f8f9fa", fg="green")
        self.lbl_answer.pack(pady=2)

    def load_data(self):
        try:
            raw_text = self.input_entry.get().strip()
            if not raw_text:
                raise ValueError
            self.heights = list(map(int, raw_text.split()))
            if not self.heights:
                raise ValueError
        except ValueError:
            messagebox.showerror("입력 오류", "올바른 숫자들을 공백으로 구분하여 입력해주세요.")
            return

        self.reset_state()
        self.btn_step.config(state=tk.NORMAL)
        self.lbl_status.config(text="데이터를 성공적으로 불러왔습니다. '다음 단계'를 눌러주세요.")
        self.draw_initial_towers()
        self.update_info()

    def reset_state(self):
        self.stack = []
        self.answer = []
        self.current_idx = 0
        self.laser_animating = False

    def reset(self):
        self.heights = []
        self.reset_state()
        self.canvas.delete("all")
        self.btn_step.config(state=tk.DISABLED)
        self.lbl_status.config(text="데이터를 불러와주세요.")
        self.update_info()

    def draw_initial_towers(self):
        self.canvas.delete("all")
        if not self.heights:
            return
            
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        
        # 화면에 그려지기 전이라면 기본값 사용
        if c_width <= 1: c_width = 850
        if c_height <= 1: c_height = 400
        
        n = len(self.heights)
        max_h = max(self.heights)
        
        bar_width = min(60, (c_width - 100) // n)
        spacing = (c_width - (bar_width * n)) // (n + 1)
        
        bottom_y = c_height - 40
        
        self.tower_coords = [] # 각 탑의 중심 x, 꼭대기 y 저장
        
        for i, h in enumerate(self.heights):
            x0 = spacing + i * (bar_width + spacing)
            x1 = x0 + bar_width
            # 픽셀 높이 계산 (최대 높이의 80%까지만)
            p_h = (h / max_h) * (c_height - 120)
            y0 = bottom_y - p_h
            y1 = bottom_y
            
            # 탑 그리기
            color = "#a0c4ff"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#80b3ff", tags=f"tower_{i}")
            
            # 탑 번호 및 높이 텍스트
            center_x = (x0 + x1) / 2
            self.canvas.create_text(center_x, y1 + 15, text=f"탑{i+1}", font=("Arial", 10, "bold"), tags=f"text_idx_{i}")
            self.canvas.create_text(center_x, y0 - 15, text=str(h), font=("Arial", 11, "bold"), tags=f"text_h_{i}")
            
            self.tower_coords.append((center_x, y0))

    def update_info(self):
        self.lbl_stack.config(text=f"스택 상태: {self.stack}")
        self.lbl_answer.config(text=f"수신 결과: {self.answer}")

    def highlight_tower(self, idx, color="#ffd6a5"):
        self.canvas.itemconfig(f"tower_{idx}", fill=color)

    def draw_laser(self, start_idx, target_idx, on_complete):
        # 레이저 애니메이션
        start_x, start_y = self.tower_coords[start_idx]
        
        if target_idx == -1:
            # 수신탑이 없는 경우 끝까지 (좌측 바깥으로) 발사
            target_x = 0
            target_y = start_y
        else:
            target_x, target_y = self.tower_coords[target_idx]
            
        laser_line = self.canvas.create_line(start_x, start_y, start_x, start_y, fill="red", width=3, dash=(4, 2), arrow=tk.LAST)
        
        steps = 15
        dx = (target_x - start_x) / steps
        dy = (target_y - start_y) / steps if target_idx != -1 else 0
        
        def animate(step=0):
            if step <= steps:
                cur_x = start_x + dx * step
                cur_y = start_y + dy * step
                self.canvas.coords(laser_line, start_x, start_y, cur_x, cur_y)
                self.after(30, lambda: animate(step + 1))
            else:
                on_complete()
                # 레이저가 너무 빨리 사라지지 않게 1초 대기 후 삭제
                self.after(800, lambda: self.canvas.delete(laser_line))
                
        animate()

    def process_pop(self):
        """스택에서 현재 탑보다 낮은 탑들을 Pop하는 과정"""
        current_height = self.heights[self.current_idx]
        
        if self.stack and self.stack[-1][1] < current_height:
            popped = self.stack.pop()
            popped_idx = popped[0] - 1
            self.highlight_tower(popped_idx, "#e5e5e5") # 회색으로 흐리게 (비활성 느낌)
            self.lbl_status.config(text=f"현재 탑({self.current_idx+1}번, 높이 {current_height})보다 수신탑({popped[0]}번, 높이 {popped[1]})이 낮아 스택에서 POP!")
            self.update_info()
            # 0.5초 대기 후 다음 Pop 확인
            self.after(600, self.process_pop)
        else:
            # Pop 과정 끝, 레이저 발사 시작
            self.shoot_laser()

    def shoot_laser(self):
        current_height = self.heights[self.current_idx]
        target_idx = -1
        target_num = 0
        
        if self.stack:
            target_num = self.stack[-1][0]
            target_idx = target_num - 1

        self.answer.append(target_num)
        
        if target_num == 0:
            self.lbl_status.config(text=f"수신할 수 있는 더 높은 탑이 없습니다. (결과: 0)")
        else:
            self.lbl_status.config(text=f"{target_num}번 탑(높이 {self.stack[-1][1]})이 레이저를 수신했습니다! (결과: {target_num})")
            
        self.update_info()
        
        def after_laser():
            # 스택에 현재 탑 추가
            self.stack.append((self.current_idx + 1, current_height))
            self.highlight_tower(self.current_idx, "#9bf6ff") # 현재 탑 강조색
            self.update_info()
            
            self.current_idx += 1
            self.laser_animating = False
            
            if self.current_idx >= len(self.heights):
                self.lbl_status.config(text="알고리즘 시각화가 완료되었습니다!")
                self.btn_step.config(state=tk.DISABLED)

        self.draw_laser(self.current_idx, target_idx, after_laser)

    def step(self):
        if self.laser_animating or self.current_idx >= len(self.heights):
            return
            
        self.laser_animating = True
        self.highlight_tower(self.current_idx, "#ffadad") # 평가 중인 탑 빨간색 느낌
        self.lbl_status.config(text=f"{self.current_idx+1}번 탑(높이 {self.heights[self.current_idx]}) 평가 시작. 좌측 방향으로 레이저 발사 준비.")
        
        # UI 업데이트 후 로직 처리 진입
        self.after(500, self.process_pop)

if __name__ == "__main__":
    app = TowerVisualizer()
    app.mainloop()
