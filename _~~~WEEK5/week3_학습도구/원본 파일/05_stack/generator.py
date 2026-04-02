class StackGenerator:
    def __init__(self, s):
        self.s = s
        
    def generate(self):
        # INIT_CODE
        code = [
            "def is_valid_parentheses(s):",
            "    stack = []",
            "    ",
            "    for i, char in enumerate(s):",
            "        if char == '(':",
            "            stack.append(char)",
            "        elif char == ')':",
            "            if len(stack) > 0:",
            "                stack.pop()",
            "            else:",
            "                return False",
            "                ",
            "    if len(stack) == 0:",
            "        return True",
            "    else:",
            "        return False"
        ]
        
        yield "INIT_CODE", code, -1, "초기화: 스택 괄호 검사 코드를 불러왔습니다."
        
        stack = []
        
        yield "INIT_VARS", {"s": self.s, "stack": stack.copy(), "idx": -1, "char": ""}, 1, "초기화: 빈 스택을 생성했습니다."

        for i, char in enumerate(self.s):
            state = {"s": self.s, "stack": stack.copy(), "idx": i, "char": char}
            yield "LOOP_NEXT", state, 3, f"문자열 순회: {i}번째 문자 '{char}' 를 확인합니다."
            
            yield "CHECK_CHAR", state, 4, f"검사: 현재 문자가 열린 괄호 '(' 인가?"
            if char == '(':
                yield "PUSH_PRE", state, 5, "열린 괄호 '(' 이므로 스택에 Push (삽입) 합니다."
                stack.append(char)
                state = {"s": self.s, "stack": stack.copy(), "idx": i, "char": char}
                yield "PUSH_DONE", state, 5, f"스택 상태: {stack}"
                
            elif char == ')':
                yield "CHECK_CHAR_CLOSE", state, 6, f"검사: 닫힌 괄호 ')' 을 발견했습니다. 스택을 검사합니다."
                
                yield "CHECK_EMPTY", state, 7, f"검사: 현재 스택에 데이터가 있는가? (len > 0)"
                if len(stack) > 0:
                    yield "POP_PRE", state, 8, f"데이터가 있으므로 스택의 가장 위(Top)에서 요소를 Pop (제거) 합니다."
                    stack.pop()
                    state = {"s": self.s, "stack": stack.copy(), "idx": i, "char": char}
                    yield "POP_DONE", state, 8, f"Pop된 후 스택 상태: {stack}"
                else:
                    yield "ERROR_EMPTY", state, 10, f"오류: 닫힌 괄호 ')' 가 나왔으나, 짝을 맞출 열린 괄호가 스택에 존재하지 않습니다."
                    return
                    
        state = {"s": self.s, "stack": stack.copy(), "idx": len(self.s), "char": ""}
        yield "LOOP_END", state, 12, "문자열 순회를 모두 마쳤습니다."
        
        yield "CHECK_FINAL", state, 12, f"검사: 스택이 비어있는가? 현재 요소 개수: {len(stack)}"
        if len(stack) == 0:
            yield "FINISHED_TRUE", state, 13, "성공 (True): 모든 괄호의 짝이 올바르게 맞았습니다!"
        else:
            yield "FINISHED_FALSE", state, 15, f"실패 (False): 짝을 찾지 못하고 남은 열린 괄호가 {len(stack)}개 있습니다."

def stack_generator(s):
    gen = StackGenerator(s)
    return gen.generate()
