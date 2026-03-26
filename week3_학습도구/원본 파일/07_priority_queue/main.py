import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import priority_queue_generator # type: ignore
from visualizer import PriorityQueueVisualizer # type: ignore

if __name__ == "__main__":
    # 응급실 환자 상태 및 우선순위 (작을 수록 높음)
    patients = [
        ("환자A (감기)", 5),
        ("환자B (골절)", 3),
        ("환자C (심정지)", 1),
        ("환자D (복통)", 4),
        ("환자E (화상)", 2)
    ]
    
    print("우선순위 큐 (Priority Queue / Heap) 시각화 도구를 실행합니다...")
    gen = priority_queue_generator(patients)
    app = PriorityQueueVisualizer(patients, generator=gen, delay=900)
    app.mainloop()
