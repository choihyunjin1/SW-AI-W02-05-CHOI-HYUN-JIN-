import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import merge_sort_generator # type: ignore
from visualizer import MergeSortVisualizer # type: ignore

if __name__ == "__main__":
    # 배열 원소가 많을 수록 분할 병합의 단계가 커짐
    arr = [38, 27, 43, 3, 9, 82, 10, 19, 56, 12, 5, 24]
    
    print("병합 정렬 (Merge Sort) 시각화 도구를 실행합니다...")
    gen = merge_sort_generator(arr)
    app = MergeSortVisualizer(arr, generator=gen, delay=400)
    app.mainloop()
