import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import divide_conquer_generator # type: ignore
from visualizer import DivideConquerVisualizer # type: ignore

if __name__ == "__main__":
    # 재귀 트리가 너무 깊거나 길어지지 않게 7개 정도의 노드 사용
    arr = [3, 5, 1, 8, 2, 9, 4]
    
    print("분할 정복 (Divide & Conquer) 시각화 도구를 실행합니다...")
    gen = divide_conquer_generator(arr)
    app = DivideConquerVisualizer(arr, generator=gen, delay=800)
    app.mainloop()
