import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import hash_table_generator # type: ignore
from visualizer import HashTableVisualizer # type: ignore

if __name__ == "__main__":
    # 추가할 초기 데이터 딕셔너리 예제
    data_pairs = [
        ("Alice", 85),
        ("Bob", 92),
        ("Charlie", 78),
        ("David", 95),
        ("Eve", 88)
    ]
    
    # 순회 조회를 시연해볼 이름 목록
    search_names = ["Bob", "Eve", "Frank"]
    
    print("해시 테이블 (dict 구현체) 시각화 도구를 실행합니다...")
    gen = hash_table_generator(data_pairs, search_names)
    app = HashTableVisualizer(data_pairs, search_names, generator=gen, delay=900)
    app.mainloop()
