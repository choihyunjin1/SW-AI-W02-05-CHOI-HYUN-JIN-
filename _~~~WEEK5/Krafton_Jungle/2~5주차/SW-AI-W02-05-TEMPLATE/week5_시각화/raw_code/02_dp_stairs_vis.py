import tkinter as tk
from tkinter import ttk, messagebox
import time

class StairsVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("DP 계단 오르기 시각화 (Bottom-Up 다이나믹 프로그래밍)")
        self.root.geometry("900x600")
        
        # 상태 변수
        self.n = 0
        self.dp = []
        self.current_i = 3
        self.boxes = {} # 캔버스 상의 배열 상자 ID
        
        self.create_widgets()
        
    def create_widgets(self):
        # 상단 컨트롤 패널
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Label(control_frame, text="계단 수 N:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.n_var = tk.StringVar(value="5")
        self.n_entry = ttk.Entry(control_frame, textvariable=self.n_var, width=5, font=("Helvetica", 12))
        self.n_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="배열 생성", command=self.init_dp).pack(side=tk.LEFT, padx=5)
        
        self.btn_next = ttk.Button(control_frame, text="다음 계산 (Next)", command=self.next_step, state=tk.DISABLED)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        
        self.btn_auto = ttk.Button(control_frame, text="자동 재생 (Auto)", command=self.auto_play, state=tk.DISABLED)
        self.btn_auto.pack(side=tk.LEFT, padx=5)
        
        # 메인 영역
        self.canvas = tk.Canvas(self.root, bg="white", height=600)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # 하단 상태 바
        self.status_var = tk.StringVar()
        self.status_var.set("대기 중... N값을 입력하고 '배열 생성'을 누르세요.")
        status_label = ttk.Label(self.root, textvariable=self.status_var, font=("Helvetica", 14, "bold"), relief=tk.SUNKEN, anchor=tk.CENTER)
        status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    def init_dp(self):
        try:
            self.n = int(self.n_var.get())
            if self.n <= 0 or self.n > 10:
                messagebox.showwarning("입력 오류", "1에서 10 사이의 값을 입력해주세요.")
                return
        except ValueError:
            messagebox.showerror("입력 오류", "유효한 숫자를 입력하세요.")
            return

        self.canvas.delete("all")
        self.boxes.clear()
        
        # DP 배열 초기화
        self.dp = [0] * (self.n + 1)
        if self.n >= 1: self.dp[1] = 1
        if self.n >= 2: self.dp[2] = 2
        
        self.current_i = 3
        
        self.draw_staircase()
        self.draw_dp_array()
        
        if self.n <= 2:
            self.status_var.set("기본 케이스(N=1 또는 2)이므로 바로 종료할 수 있습니다.")
            self.btn_next.config(state=tk.DISABLED)
            self.btn_auto.config(state=tk.DISABLED)
        else:
            self.status_var.set("초기 상태: dp[1] = 1, dp[2] = 2")
            self.btn_next.config(state=tk.NORMAL)
            self.btn_auto.config(state=tk.NORMAL)
            
    def draw_staircase(self):
        # 계단을 좌측 하단에서 우측 상단으로 그리기
        start_x, start_y = 50, 350
        step_w, step_h = 40, 30
        
        for i in range(1, self.n + 1):
            x1 = start_x + (i-1) * step_w
            y1 = start_y - i * step_h
            x2 = x1 + step_w
            y2 = start_y
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline="black")
            # 계단 번호 텍스트
            self.canvas.create_text(x1 + step_w//2, y1 - 15, text=f"{i}", font=("Helvetica", 10, "bold"))
            
    def draw_dp_array(self):
        # 배열을 가로 상자들로 표시 (상향식 구조 강조)
        start_x, start_y = 50, 450 # 계단 밑으로 이동
        box_w, box_h = 60, 60
        
        self.canvas.create_text(start_x, start_y - 30, text="DP 배열 메모리 (Bottom-Up):", anchor=tk.W, font=("Helvetica", 12, "bold"))
        
        for i in range(1, self.n + 1):
            x1 = start_x + (i-1) * box_w
            y1 = start_y
            x2 = x1 + box_w
            y2 = start_y + box_h
            
            # 초기값 1, 2는 채워져 있음
            fill_color = "skyblue" if i <= 2 else "white"
            val_text = str(self.dp[i]) if i <= 2 else "?"
            
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")
            idx_txt = self.canvas.create_text(x1 + box_w//2, y1 - 10, text=f"dp[{i}]")
            val_txt = self.canvas.create_text(x1 + box_w//2, y1 + box_h//2, text=val_text, font=("Helvetica", 14, "bold"))
            
            self.boxes[i] = {"rect": rect, "val_txt": val_txt, "x1": x1, "y1": y1, "x2": x2, "y2": y2}
            
    def next_step(self):
        if self.current_i > self.n:
            self.status_var.set("모든 DP 배열 계산이 완료되었습니다.")
            self.btn_next.config(state=tk.DISABLED)
            self.btn_auto.config(state=tk.DISABLED)
            
            # 정답 강조
            ans_box = self.boxes[self.n]
            self.canvas.itemconfig(ans_box["rect"], fill="gold", width=3, outline="red")
            messagebox.showinfo("계산 완료", f"{self.n}번째 계단을 오르는 방법의 수는 {self.dp[self.n]}입니다.")
            return
            
        i = self.current_i
        
        # 이전 하이라이트 지우기
        for k in range(1, i-2):
           if k in self.boxes:
               self.canvas.itemconfig(self.boxes[k]["rect"], fill="lightgray")
               
        # 사용할 두 이전 값 하이라이트
        self.canvas.itemconfig(self.boxes[i-1]["rect"], fill="lightgreen")
        self.canvas.itemconfig(self.boxes[i-2]["rect"], fill="lightgreen")
        
        # 합 계산
        self.dp[i] = self.dp[i-1] + self.dp[i-2]
        
        # 화살표 그리기 (i-2 -> i, i-1 -> i)
        px1, py1 = self.boxes[i-2]["x1"] + 30, self.boxes[i-2]["y2"]
        px2, py2 = self.boxes[i-1]["x1"] + 30, self.boxes[i-1]["y2"]
        tx, ty = self.boxes[i]["x1"] + 30, self.boxes[i]["y2"] + 30
        
        self.canvas.create_line(px1, py1, tx-10, ty, arrow=tk.LAST, fill="gray", dash=(4, 4))
        self.canvas.create_line(px2, py2, tx+10, ty, arrow=tk.LAST, fill="gray", dash=(4, 4))
        self.canvas.create_line(tx, ty, tx, self.boxes[i]["y2"], arrow=tk.LAST, fill="red")
        
        # 계산된 현재 박스 갱신
        self.canvas.itemconfig(self.boxes[i]["rect"], fill="orange")
        self.canvas.itemconfig(self.boxes[i]["val_txt"], text=str(self.dp[i]))
        
        self.status_var.set(f"dp[{i}] = dp[{i-1}] ({self.dp[i-1]}) + dp[{i-2}] ({self.dp[i-2]}) => {self.dp[i]}")
        
        self.current_i += 1
        
    def auto_play(self):
        if self.current_i <= self.n:
            self.next_step()
            self.root.after(1000, self.auto_play)
            
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    app = StairsVisualizer(root)
    root.mainloop()
