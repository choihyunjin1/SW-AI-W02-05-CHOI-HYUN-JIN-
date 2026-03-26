class LinkedListGenerator:
    def __init__(self, values_to_append):
        self.values = values_to_append
        
    def generate(self):
        # INIT_CODE
        code = [
            "class Node:",
            "    def __init__(self, data):",
            "        self.data = data",
            "        self.next = None",
            "",
            "class LinkedList:",
            "    def __init__(self):",
            "        self.head = None",
            "",
            "    def append(self, data):",
            "        new_node = Node(data)",
            "        if self.head is None:",
            "            self.head = new_node",
            "            return",
            "        ",
            "        current = self.head",
            "        while current.next is None:",
            "            current = current.next",
            "        ",
            "        current.next = new_node",
            "",
            "    def print_list(self):",
            "        values = []",
            "        current = self.head",
            "        while current is not None:",
            "            values.append(current.data)",
            "            current = current.next",
            "        return values"
        ]
        yield "INIT_CODE", code, -1, "초기화: 연결 리스트(Linked List) 클래스 코드를 불러왔습니다."
        
        # 실제 파이썬 구현체 흉내
        nodes = [] # 각 요소를 사전으로 표현: {"id": "obj_id", "data": val, "next_id": None}
        head_id = None
        
        yield "INIT_LL", self.get_state(nodes, head_id), 7, "초기 빈 연결 리스트(LinkedList) 인스턴스를 생성했습니다."
        
        # Append Phase
        for val in self.values:
            yield "APPEND_CALL", self.get_state(nodes, head_id, current_action_data=val), 9, f"메소드 호출: 리스트 끝에 값 '{val}'을(를) 추가(append) 시도합니다."
            
            new_id = f"node_{len(nodes)}"
            new_node = {"id": new_id, "data": val, "next_id": None}
            yield "CREATE_NODE", self.get_state(nodes, head_id, current_action_data=val, new_node_id=new_id), 10, f"메모리 상에 새로운 Node(data={val})를 할당했습니다."
            
            # (nodes 배열에 임시로 노드를 넣지만 아직 연결 안 된 상태 표현용으로 사용)
            temp_nodes = nodes.copy()
            temp_nodes.append(new_node)
            
            yield "CHECK_HEAD", self.get_state(temp_nodes, head_id, current_action_data=val, new_node_id=new_id), 11, f"검사: 현재 연결 리스트의 시작점(head)이 비어있는가?"
            
            if head_id is None:
                yield "SET_HEAD", self.get_state(temp_nodes, head_id, current_action_data=val, new_node_id=new_id, head_ptr_changing=True), 12, "head가 비어있으므로 새 노드를 바로 head로 지정합니다."
                head_id = new_id
                nodes = temp_nodes # 확정
                yield "APPEND_DONE_HEAD", self.get_state(nodes, head_id, current_action_data=val), 13, f"값 '{val}' 추가 완료. (첫 번째 노드)"
            else:
                yield "SET_CURR_HEAD", self.get_state(temp_nodes, head_id, current_action_data=val, new_node_id=new_id, curr_ptr_id=head_id), 15, "head가 존재합니다. 가장 마지막 노드를 찾기 위해 탐색 포인터 'current'를 head에 둡니다."
                curr_id = head_id
                
                while True:
                    # 현재 curr_id의 next 검사
                    curr_idx = -1
                    for i, node in enumerate(temp_nodes):
                        if node["id"] == curr_id:
                            curr_idx = i
                            break
                    
                    yield "CHECK_NEXT", self.get_state(temp_nodes, head_id, current_action_data=val, new_node_id=new_id, curr_ptr_id=curr_id), 16, f"검사: 현재 노드({temp_nodes[curr_idx]['data']})의 next 가 비어있는가?"
                    
                    if temp_nodes[curr_idx]["next_id"] is None:
                        yield "FOUND_LAST", self.get_state(temp_nodes, head_id, current_action_data=val, new_node_id=new_id, curr_ptr_id=curr_id), 18, f"next가 비어있습니다. 이 노드가 마지막 노드입니다."
                        break
                    else:
                        yield "MOVE_CURR", self.get_state(temp_nodes, head_id, current_action_data=val, new_node_id=new_id, curr_ptr_id=curr_id), 17, "next가 존재하므로 포인터 'current'를 다음 노드로 이동시킵니다."
                        curr_id = temp_nodes[curr_idx]["next_id"]
                
                # curr_id 의 next를 new_id로
                for node in temp_nodes:
                    if node["id"] == curr_id:
                        node["next_id"] = new_id
                        break
                nodes = temp_nodes
                yield "APPEND_DONE_LINK", self.get_state(nodes, head_id, current_action_data=val, new_node_id=new_id, curr_ptr_id=curr_id, link_changing=curr_id), 19, f"마지막 노드의 next를 새 노드와 연결하여 '{val}' 추가를 완료합니다."

        yield "APPEND_ALL_DONE", self.get_state(nodes, head_id), -1, "모든 노드 추가가 완료되었습니다. 이제 리스트 전체를 순회해볼까요?"
        
        # Print Phase
        yield "PRINT_CALL", self.get_state(nodes, head_id), 21, "메소드 호출: 리스트의 모든 값을 순회 출력하기 위해 print_list()를 실행합니다."
        
        res_values = []
        yield "PRINT_INIT", self.get_state(nodes, head_id, res_values=res_values.copy()), 22, "값을 담을 빈 배열(values)을 준비합니다."
        
        curr_id = head_id
        yield "PRINT_CURR_HEAD", self.get_state(nodes, head_id, res_values=res_values.copy(), curr_ptr_id=curr_id), 23, "순회 탐색자 'current'를 시작점인 head에 맞춥니다."
        
        while True:
            yield "PRINT_CHECK_CURR", self.get_state(nodes, head_id, res_values=res_values.copy(), curr_ptr_id=curr_id), 24, "검사: 탐색 포인터 'current'가 비어있지 않은가? (노드의 끝에 도달했는가?)"
            
            if curr_id is None:
                yield "PRINT_CURR_NONE", self.get_state(nodes, head_id, res_values=res_values.copy(), curr_ptr_id=curr_id), 27, "탐색 포인터가 비어있습니다(순회 종료)."
                break
                
            curr_data = None
            for node in nodes:
                if node["id"] == curr_id:
                    curr_data = node["data"]
                    break
                    
            res_values.append(curr_data)
            yield "PRINT_APPEND", self.get_state(nodes, head_id, res_values=res_values.copy(), curr_ptr_id=curr_id, current_action_data=curr_data), 25, f"현재 노드의 값 '{curr_data}'를 배열에 담습니다. (출력)"
            
            # 옮기기 전
            next_id = None
            for node in nodes:
                if node["id"] == curr_id:
                    next_id = node["next_id"]
                    break
                    
            yield "PRINT_MOVE", self.get_state(nodes, head_id, res_values=res_values.copy(), curr_ptr_id=curr_id), 26, "다음 요소를 살펴보기 위해 탐색 포인터 'current'를 next를 따라 한 칸 이동합니다."
            curr_id = next_id


        yield "FINISHED", self.get_state(nodes, head_id, res_values=res_values.copy()), 28, f"최종 결과 데이터: {res_values} 를 리턴하고 종료합니다."


    def get_state(self, nodes, head_id, current_action_data=None, new_node_id=None, curr_ptr_id=None, head_ptr_changing=False, link_changing=None, res_values=None):
        import copy
        return {
            "nodes": copy.deepcopy(nodes),
            "head_id": head_id,
            "current_action_data": current_action_data,
            "new_node_id": new_node_id,
            "curr_ptr_id": curr_ptr_id,
            "head_ptr_changing": head_ptr_changing,
            "link_changing": link_changing,
            "res_values": res_values
        }

def linked_list_generator(values):
    gen = LinkedListGenerator(values)
    return gen.generate()
