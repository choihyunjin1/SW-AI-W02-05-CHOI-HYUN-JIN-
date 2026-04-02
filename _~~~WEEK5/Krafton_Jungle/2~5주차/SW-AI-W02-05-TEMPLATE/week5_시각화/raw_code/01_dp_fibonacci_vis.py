import tkinter as tk
from tkinter import ttk, messagebox

# 피보나치 실행 이벤트를 추적하기 위한 제너레이터
def trace_fibonacci(n):
    memo = {}
    events = []
    
    # 노드 ID를 순차적으로 부여하기 위한 변수
    node_counter = 0

    def fib(k, parent_id=None, depth=0):
        nonlocal node_counter
        my_id = node_counter
        node_counter += 1
        
        events.append({
            "type": "call",
            "k": k,
            "id": my_id,
            "parent": parent_id,
            "depth": depth,
            "desc": f"fib({k}) 호출"
        })
        
        if k in memo:
            events.append({
                "type": "memo_hit",
                "k": k,
                "val": memo[k],
                "id": my_id,
                "desc": f"✨ memo[{k}]에 저장된 값({memo[k]}) 바로 반환 (중복 계산 방지)"
            })
            return memo[k]
        
        if k == 0:
            memo[0] = 0
            events.append({"type": "base_case", "k": k, "val": 0, "id": my_id, "desc": "기본 케이스: fib(0) = 0"})
            events.append({"type": "memo_update", "k": k, "val": 0, "desc": f"memo[0] = 0 추가"})
            return 0
        
        if k == 1:
            memo[1] = 1
            events.append({"type": "base_case", "k": k, "val": 1, "id": my_id, "desc": "기본 케이스: fib(1) = 1"})
            events.append({"type": "memo_update", "k": k, "val": 1, "desc": f"memo[1] = 1 추가"})
            return 1
            
        # 재귀 호출 과정 (하향식)
        v1 = fib(k - 1, my_id, depth + 1)
        v2 = fib(k - 2, my_id, depth + 1)
        
        result = v1 + v2
        memo[k] = result
        
        events.append({
            "type": "calc_done",
            "k": k,
            "val": result,
            "id": my_id,
            "desc": f"계산 완료: fib({k}) = {v1} + {v2} = {result}"
        })
        events.append({"type": "memo_update", "k": k, "val": result, "desc": f"memo[{k}] = {result} 추가 및 저장"})
        return result

    fib(n)
    return events

class FibonacciVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("DP 피보나치 수열 시각화 (Memoization)")
        self.root.geometry("1000x800")
        
        # 상태 변수
        self.events = []
        self.current_step = 0
        self.nodes = {}      # id -> {x, y, oval, text, line}
        self.memo_data = {}  # 현재 시점의 memo
        
        self.create_widgets()
        
    def create_widgets(self):
        # 상단 컨트롤 패널
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Label(control_frame, text="N (권장 3~6):", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.n_var = tk.StringVar(value="5")
        self.n_entry = ttk.Entry(control_frame, textvariable=self.n_var, width=5, font=("Helvetica", 12))
        self.n_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="시작/생성", command=self.start_visualization).pack(side=tk.LEFT, padx=5)
        
        self.btn_next = ttk.Button(control_frame, text="다음 단계 (Next)", command=self.next_step, state=tk.DISABLED)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        
        self.btn_auto = ttk.Button(control_frame, text="자동 재생 (Auto)", command=self.auto_play, state=tk.DISABLED)
        self.btn_auto.pack(side=tk.LEFT, padx=5)
        
        # 메인 영역 (트리, 메모)
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # 트리 캔버스 영역 (스크롤바 추가)
        canvas_frame = ttk.Frame(main_paned)
        main_paned.add(canvas_frame, weight=3)
        self.canvas_sx = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        self.canvas_sy = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(canvas_frame, bg="white", xscrollcommand=self.canvas_sx.set, yscrollcommand=self.canvas_sy.set)
        self.canvas_sx.config(command=self.canvas.xview)
        self.canvas_sy.config(command=self.canvas.yview)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas_sx.grid(row=1, column=0, sticky="ew")
        self.canvas_sy.grid(row=0, column=1, sticky="ns")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # 메모이제이션 표시 영역
        memo_frame = ttk.LabelFrame(main_paned, text="Memoization 테이블 (캐시)", padding=10)
        main_paned.add(memo_frame, weight=1)
        
        self.memo_tree = ttk.Treeview(memo_frame, columns=("Key", "Value"), show="headings", height=20)
        self.memo_tree.heading("Key", text="N")
        self.memo_tree.heading("Value", text="fib(N)")
        self.memo_tree.column("Key", width=50, anchor=tk.CENTER)
        self.memo_tree.column("Value", width=100, anchor=tk.CENTER)
        self.memo_tree.pack(expand=True, fill=tk.BOTH)
        
        # 하단 상태 바
        self.status_var = tk.StringVar()
        self.status_var.set("대기 중... N값을 입력하고 '시작/생성'을 누르세요.")
        status_label = ttk.Label(self.root, textvariable=self.status_var, font=("Helvetica", 12, "bold"), relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
    def start_visualization(self):
        try:
            n = int(self.n_var.get())
            if n < 0 or n > 8:
                messagebox.showwarning("입력 오류", "0에서 8 사이의 값을 입력해주세요. (그 이상은 화면이 좁습니다)")
                return
        except ValueError:
            messagebox.showerror("입력 오류", "유효한 숫자를 입력하세요.")
            return
            
        # 초기화
        self.canvas.delete("all")
        for item in self.memo_tree.get_children():
            self.memo_tree.delete(item)
        
        self.events = trace_fibonacci(n)
        self.current_step = 0
        self.nodes = {}
        self.memo_data = {}
        
        self.btn_next.config(state=tk.NORMAL)
        self.btn_auto.config(state=tk.NORMAL)
        self.status_var.set(f"준비 완료! 총 {len(self.events)}단계가 감지되었습니다. 다음 단계를 누르세요.")
        
    def next_step(self):
        if self.current_step >= len(self.events):
            self.status_var.set("시각화가 모두 완료되었습니다.")
            self.btn_next.config(state=tk.DISABLED)
            self.btn_auto.config(state=tk.DISABLED)
            return

        event = self.events[self.current_step]
        ev_type = event["type"]
        
        # 상태 메세지 업데이트
        if "desc" in event:
            self.status_var.set(f"[단계 {self.current_step + 1}/{len(self.events)}] " + event["desc"])
            
        if ev_type == "call":
            self.draw_node(event["id"], event["k"], event["parent"], event["depth"])
        elif ev_type == "memo_hit":
            nid = event["id"]
            if nid in self.nodes:
                self.canvas.itemconfig(self.nodes[nid]["oval"], fill="lightgreen", outline="green", width=3)
                self.canvas.itemconfig(self.nodes[nid]["text"], text=f"fib({event['k']})\\n-> {event['val']}")
        elif ev_type == "base_case":
            nid = event["id"]
            if nid in self.nodes:
                self.canvas.itemconfig(self.nodes[nid]["oval"], fill="skyblue")
                self.canvas.itemconfig(self.nodes[nid]["text"], text=f"fib({event['k']})\\n-> {event['val']}")
        elif ev_type == "calc_done":
            nid = event["id"]
            if nid in self.nodes:
                self.canvas.itemconfig(self.nodes[nid]["oval"], fill="orange")
                self.canvas.itemconfig(self.nodes[nid]["text"], text=f"fib({event['k']})\\n-> {event['val']}")
        elif ev_type == "memo_update":
            k, val = event["k"], event["val"]
            if k not in self.memo_data:
                self.memo_data[k] = val
                self.memo_tree.insert("", "end", iid=str(k), values=(k, val))
                # 하이라이트 효과 후 제거
                self.memo_tree.selection_set(str(k))
                self.root.after(500, lambda: self.memo_tree.selection_remove(str(k)))
                
        self.current_step += 1
        
    def auto_play(self):
        if self.current_step < len(self.events):
            self.next_step()
            self.root.after(500, self.auto_play) # 0.5초 간격으로 자동 실행
            
    def draw_node(self, node_id, k, parent_id, depth):
        # 기본 좌표 설정 로직 (스크롤 대응 넓은 가상 영역)
        y = 50 + depth * 80
        
        if parent_id is None:
            x = 1000 # 최상단 루트 노드를 x=1000에 배치
        else:
            parent_x = self.nodes[parent_id]["x"]
            # 부모의 왼쪽 자식(n-1)인지 오른쪽 자식(n-2)인지 판단 (간단히)
            # 트리가 겹치지 않게 depth에 따라 간격을 줄임
            offset = max(1200 // (2 ** (depth + 1)), 50)
            
            # 여기서 부모의 이전 자식이 있는지 확인
            sibling_exists = any(nd["parent"] == parent_id for nd in self.nodes.values())
            if sibling_exists:
                x = parent_x + offset  # 오른쪽 자식 (n-2)
            else:
                x = parent_x - offset  # 왼쪽 자식 (n-1)
                
        # 선 그리기
        if parent_id is not None:
            px, py = self.nodes[parent_id]["x"], self.nodes[parent_id]["y"]
            line = self.canvas.create_line(px, py+20, x, y-20, arrow=tk.LAST, fill="gray")
        else:
            line = None
            
        # 노드 (원) 그리기
        r = 25
        oval = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="white", outline="black", width=2)
        text = self.canvas.create_text(x, y, text=f"fib({k})", font=("Helvetica", 10, "bold"))
        
        self.nodes[node_id] = {
            "x": x, "y": y,
            "oval": oval, "text": text,
            "line": line,
            "parent": parent_id
        }
        
        # 스크롤 영역 자동 갱신
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    
    # 테마 설정 (보다 모던한 느낌으로)
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
        
    app = FibonacciVisualizer(root)
    root.mainloop()
