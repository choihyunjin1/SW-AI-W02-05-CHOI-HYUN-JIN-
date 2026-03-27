import tkinter as tk
from tkinter import ttk

class MeetingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("그리디 회의실 배정 시각화 (종료 시간 기준 정렬)")
        self.root.geometry("1000x800")
        
        # 원본 데이터 및 화면 요소 관리
        self.raw_meetings = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10), (8, 11), (8, 12), (2, 13), (12, 14)]
        self.meetings = []
        self.events = []
        self.event_idx = 0
        self.last_end = 0
        self.selected = []
        
        self.create_widgets()
        
    def create_widgets(self):
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Button(control_frame, text="시작 (데이터 로드 / 재설정)", command=self.start_visualization).pack(side=tk.LEFT, padx=5)
        self.btn_next = ttk.Button(control_frame, text="다음 단계 (Next)", command=self.next_step, state=tk.DISABLED)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        self.btn_auto = ttk.Button(control_frame, text="자동 재생 (Auto)", command=self.auto_play, state=tk.DISABLED)
        self.btn_auto.pack(side=tk.LEFT, padx=5)
        
        self.canvas = tk.Canvas(self.root, bg="white", height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.status_var = tk.StringVar()
        self.status_var.set("대기 중... '시작' 버튼을 누르세요.")
        lbl_status = ttk.Label(self.root, textvariable=self.status_var, font=("Helvetica", 14), relief=tk.SUNKEN, anchor=tk.W)
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
    def draw_timeline_grid(self):
        self.canvas.delete("all")
        # x 타임라인: 0부터 16까지
        self.pad_x = 50
        self.unit_w = 55 # 1시간당 픽셀수 (텍스트 안 겹치게 늘림)
        self.pad_y = 50
        
        for t in range(16):
            x = self.pad_x + t * self.unit_w
            self.canvas.create_line(x, self.pad_y, x, 600, fill="lightgray", dash=(2,2))
            self.canvas.create_text(x, self.pad_y - 20, text=f"{t}시", font=("Helvetica", 10))
            
    def start_visualization(self):
        self.draw_timeline_grid()
        self.rects = {} 
        
        # 1단계: 정렬 전 초기 상태 그리기
        self.status_var.set("1. 초기 회의 상태 (정렬 전)")
        
        # 회의 그리기 (랜덤하게 y축 분산)
        for i, (start, end) in enumerate(self.raw_meetings):
            x1 = self.pad_x + start * self.unit_w
            x2 = self.pad_x + end * self.unit_w
            y1 = self.pad_y + i * 40
            y2 = y1 + 30
            
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="skyblue", outline="blue")
            txt = self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=f"({start}~{end})")
            self.rects[i] = {"rect": rect, "txt": txt, "data": (start, end), "y_idx": i}
            
        self.events = [{"action": "sort", "msg": "그리디 알고리즘 적용을 위해 '종료 시간' 기준으로 회의를 정렬합니다."}]
        
        sorted_meetings = sorted(enumerate(self.raw_meetings), key=lambda x: x[1][1])
        
        # 정렬 후 그리디 과정 이벤트 생성
        for idx_in_sorted, (orig_id, (start, end)) in enumerate(sorted_meetings):
            self.events.append({"action": "check", "id": orig_id, "start": start, "end": end, "msg": f"회의({start}~{end}) 검토 중..."})
            self.events.append({"action": "eval", "id": orig_id, "start": start, "end": end, "msg": ""})
            
        self.event_idx = 0
        self.btn_next.config(state=tk.NORMAL)
        self.btn_auto.config(state=tk.NORMAL)
        self.last_end = 0
        self.selected = []
        
    def next_step(self):
        if self.event_idx >= len(self.events):
            self.status_var.set(f"모든 탐색 완료. 선택된 회의: {self.selected} (총 {len(self.selected)}개)")
            self.btn_next.config(state=tk.DISABLED)
            self.btn_auto.config(state=tk.DISABLED)
            return
            
        ev = self.events[self.event_idx]
        action = ev["action"]
        
        if action == "sort":
            self.status_var.set(ev["msg"])
            # 위치 재배열 (종료 시간 순서)
            sorted_m = sorted(self.rects.items(), key=lambda item: item[1]["data"][1])
            for new_y_idx, (orig_id, info) in enumerate(sorted_m):
                old_y1 = self.pad_y + info["y_idx"] * 40
                new_y1 = self.pad_y + new_y_idx * 40
                dy = new_y1 - old_y1
                
                self.canvas.move(info["rect"], 0, dy)
                self.canvas.move(info["txt"], 0, dy)
                info["y_idx"] = new_y_idx # 업데이트
                
        elif action == "check":
            self.status_var.set(ev["msg"])
            rid = ev["id"]
            self.canvas.itemconfig(self.rects[rid]["rect"], outline="red", width=3)
            
        elif action == "eval":
            rid = ev["id"]
            start, end = ev["start"], ev["end"]
            
            if start >= self.last_end:
                self.selected.append((start, end))
                self.last_end = end
                self.status_var.set(f"선택 완료: 시작 시간({start})이 현재 시간({self.last_end - end + start})보다 크거나 같음.")
                self.canvas.itemconfig(self.rects[rid]["rect"], fill="lightgreen", outline="green", width=3)
                
                # 타임라인을 가로지르는 수직 파란 선(현재 종료 시간) 그리기
                self.canvas.delete("current_time_line")
                x = self.pad_x + self.last_end * self.unit_w
                self.canvas.create_line(x, self.pad_y, x, 600, fill="blue", width=2, dash=(4,2), tags="current_time_line")
                self.canvas.create_text(x, self.pad_y - 35, text="현재시간", fill="blue", tags="current_time_line")
            else:
                self.status_var.set(f"거절됨: 시작 시간({start})이 현재 시간({self.last_end})보다 이름.")
                self.canvas.itemconfig(self.rects[rid]["rect"], fill="#DDDDDD", outline="gray", width=1)
                
        self.event_idx += 1
            
    def auto_play(self):
        if self.event_idx < len(self.events):
            self.next_step()
            self.root.after(600, self.auto_play)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    app = MeetingVisualizer(root)
    root.mainloop()
