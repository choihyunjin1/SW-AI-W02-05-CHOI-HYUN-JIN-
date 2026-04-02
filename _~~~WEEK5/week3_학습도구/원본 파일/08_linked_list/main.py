import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import linked_list_generator # type: ignore
from visualizer import LinkedListVisualizer # type: ignore

if __name__ == "__main__":
    # 추가할 데이터 리스트
    values = [10, 20, 30, 40]
    
    print("연결 리스트 (Linked List) 시각화 도구를 실행합니다...")
    gen = linked_list_generator(values)
    app = LinkedListVisualizer(values, generator=gen, delay=900)
    app.mainloop()
