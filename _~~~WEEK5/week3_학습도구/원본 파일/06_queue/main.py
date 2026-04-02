import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import queue_generator # type: ignore
from visualizer import QueueVisualizer # type: ignore

if __name__ == "__main__":
    # 프린트 작업 리스트
    jobs = ["문서A", "보고서", "사진", "계약서"]
    
    print("큐 (Queue) 시각화 도구를 실행합니다...")
    gen = queue_generator(jobs)
    app = QueueVisualizer(jobs, generator=gen, delay=900)
    app.mainloop()
