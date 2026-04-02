import sys
import os

# 현재 스크립트의 경로를 구합니다.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import binary_search_generator # type: ignore
from visualizer import BinarySearchVisualizer # type: ignore

if __name__ == "__main__":
    # 데이터 개수를 늘려 여러 번 분할되는 과정을 볼 수 있게 구성
    arr = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
    target = 26 # 우측, 그리고 좌측 탐색을 거치는 값
    
    print("이분 탐색 (Binary Search) 시각화 도구를 실행합니다...")
    gen = binary_search_generator(arr, target)
    app = BinarySearchVisualizer(arr, target, generator=gen, delay=900)
    app.mainloop()
