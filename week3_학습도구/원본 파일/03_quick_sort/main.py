# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox, simpledialog

from generator import quick_sort_generator # type: ignore
from visualizer import QuickSortVisualizer # type: ignore

def main():
    root = tk.Tk()
    root.withdraw() 
    
    # 예제 10, 7, 8, 9, 1, 5
    A = [10, 7, 8, 9, 1, 5]

    choice = messagebox.askyesno(
        "데이터 설정", 
        "기본 예제를 사용하시겠습니까?\narr = [10, 7, 8, 9, 1, 5]"
    )
    
    if not choice: # 아니오를 고르면 직접 입력
        in_str = simpledialog.askstring("입력", "정렬할 숫자들을 공백으로 구분하여 입력하세요: ")
        if in_str:
            try:
                tokens = list(map(int, in_str.strip().split()))
                if not tokens: return
                A = tokens
            except ValueError:
                messagebox.showerror("오류", "잘못된 입력입니다. 숫자만 입력해주세요.")
                return
        else:
            return

    speed_str = simpledialog.askstring("시각화 딜레이 설정", "애니메이션 딜레이(ms)를 입력하세요:\n(기본 350, 작을수록 속도가 빠름)")
    delay = 350
    if speed_str and isinstance(speed_str, str) and speed_str.isdigit():
        delay = int(speed_str)
        
    generator = quick_sort_generator(A)
    
    app = QuickSortVisualizer(A, generator, delay=delay)
    app.mainloop()

if __name__ == "__main__":
    main()
