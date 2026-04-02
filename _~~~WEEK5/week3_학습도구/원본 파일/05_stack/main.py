import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator import stack_generator # type: ignore
from visualizer import StackVisualizer # type: ignore

if __name__ == "__main__":
    # 괄호 짝 검사 문자열 설정
    test_str = "((()()))"
    
    print("스택 (Stack) 시각화 도구를 실행합니다...")
    gen = stack_generator(test_str)
    app = StackVisualizer(test_str, generator=gen, delay=700)
    app.mainloop()
