import tkinter as tk
from tkinter import ttk, messagebox

class GreedyCoinVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("그리디 거스름돈 시각화 (큰 동전부터 선택)")
        self.root.geometry("800x600")
        
        self.coins = [500, 100, 50, 10]
        self.current_coin_idx = 0
        self.change_amount = 0
        self.result = {500:0, 100:0, 50:0, 10:0}
        self.events = []
        self.event_idx = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        # 상단 컨트롤 패널
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Label(control_frame, text="거스를 금액(10단위):", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.amount_var = tk.StringVar(value="1260")
        self.amount_entry = ttk.Entry(control_frame, textvariable=self.amount_var, width=10, font=("Helvetica", 12))
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="시작", command=self.start_visualization).pack(side=tk.LEFT, padx=5)
        
        self.btn_next = ttk.Button(control_frame, text="다음 단계 (Next)", command=self.next_step, state=tk.DISABLED)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        
        self.btn_auto = ttk.Button(control_frame, text="자동 재생 (Auto)", command=self.auto_play, state=tk.DISABLED)
        self.btn_auto.pack(side=tk.LEFT, padx=5)
        
        # 메인 정보 표시 영역
        info_frame = ttk.Frame(self.root, padding=20)
        info_frame.pack(fill=tk.X)
        
        self.remain_var = tk.StringVar()
        self.remain_var.set("남은 금액: 0 원")
        ttk.Label(info_frame, textvariable=self.remain_var, font=("Helvetica", 24, "bold"), foreground="blue").pack(side=tk.TOP, pady=10)
        
        # 캔버스 영역 (동전 표시)
        self.canvas = tk.Canvas(self.root, bg="white", height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 하단 상태 바
        self.status_var = tk.StringVar()
        self.status_var.set("대기 중... 금액을 입력하고 '시작'을 누르세요.")
        lbl_status = ttk.Label(self.root, textvariable=self.status_var, font=("Helvetica", 14), relief=tk.SUNKEN, anchor=tk.W)
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
    def start_visualization(self):
        try:
            amount = int(self.amount_var.get())
            if amount < 0 or amount % 10 != 0:
                messagebox.showwarning("입력 오류", "금액은 10원 단위 양수여야 합니다.")
                return
        except ValueError:
            messagebox.showerror("입력 오류", "유효한 숫자를 입력하세요.")
            return
            
        self.change_amount = amount
        self.remain_var.set(f"남은 금액: {amount} 원")
        self.result = {500:0, 100:0, 50:0, 10:0}
        self.canvas.delete("all")
        
        self.events = self.generate_events(amount)
        self.event_idx = 0
        
        self.btn_next.config(state=tk.NORMAL)
        self.btn_auto.config(state=tk.NORMAL)
        self.status_var.set(f"{amount}원 거스름돈 계산을 시작합니다. (사용 동전: 500, 100, 50, 10)")
        
        self.draw_coin_panels()
        
    def generate_events(self, amount):
        events = []
        remain = amount
        for coin in self.coins:
            events.append({"action": "focus", "coin": coin, "msg": f"{coin}원 동전 적용 검토 중..."})
            
            cnt = remain // coin
            if cnt > 0:
                for i in range(cnt):
                    remain -= coin
                    events.append({"action": "add_coin", "coin": coin, "remain": remain, "msg": f"{coin}원 동전 1개 추가! (남은 돈: {remain}원)"})
            events.append({"action": "complete_coin", "coin": coin, "remain": remain, "msg": f"{coin}원 동전 적용 완료. (현재 남은 돈: {remain}원)"})
            if remain == 0:
                break
        return events
        
    def draw_coin_panels(self):
        # 캔버스에 500, 100, 50, 10 각 구역을 나눔
        c_width = 760
        section_w = c_width // 4
        self.panels = {}
        for i, coin in enumerate(self.coins):
            x1 = i * section_w
            x2 = x1 + section_w
            self.canvas.create_rectangle(x1, 0, x2, 300, fill="lightgray", outline="gray", dash=(4,4), tags=f"panel_{coin}")
            self.canvas.create_text(x1 + section_w//2, 20, text=f"{coin}원", font=("Helvetica", 16, "bold"))
            
            self.panels[coin] = {"x_center": x1 + section_w//2, "y_start": 50, "count": 0}
            
    def next_step(self):
        if self.event_idx >= len(self.events):
            self.status_var.set("계산 완료! 그리디 알고리즘에 의해 최소 개수의 동전이 선택되었습니다.")
            self.btn_next.config(state=tk.DISABLED)
            self.btn_auto.config(state=tk.DISABLED)
            return
            
        ev = self.events[self.event_idx]
        action = ev["action"]
        coin = ev["coin"]
        msg = ev["msg"]
        
        self.status_var.set(msg)
        
        if action == "focus":
            # 이전 포커스를 지우고 현재 동전 영역 하이라이트
            for c in self.coins:
                self.canvas.itemconfig(f"panel_{c}", fill="lightgray", outline="gray", width=1)
            self.canvas.itemconfig(f"panel_{coin}", fill="lightyellow", outline="orange", width=3)
            
        elif action == "add_coin":
            self.change_amount = ev["remain"]
            self.remain_var.set(f"남은 금액: {self.change_amount} 원")
            
            self.result[coin] += 1
            idx = self.panels[coin]["count"]
            col = idx % 2
            row = idx // 2
            xc = self.panels[coin]["x_center"] - 20 + col * 40
            y = self.panels[coin]["y_start"] + row * 40
            self.panels[coin]["count"] += 1
            
            # 동전 그리기
            r = 20
            color = "gold" if coin >= 100 else "silver"
            self.canvas.create_oval(xc-r, y-r, xc+r, y+r, fill=color, outline="black")
            self.canvas.create_text(xc, y, text=str(coin), font=("Helvetica", 10, "bold"))
            
        elif action == "complete_coin":
            self.canvas.itemconfig(f"panel_{coin}", fill="#E8F8F5", outline="green", width=2)
            
        self.event_idx += 1
        
    def auto_play(self):
        if self.event_idx < len(self.events):
            self.next_step()
            self.root.after(400, self.auto_play)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    app = GreedyCoinVisualizer(root)
    root.mainloop()
