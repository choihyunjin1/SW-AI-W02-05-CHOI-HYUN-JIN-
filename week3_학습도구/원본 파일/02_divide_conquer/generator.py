class DivideConquerGenerator:
    def __init__(self, arr, start, end):
        self.arr = arr
        self.start = start
        self.end = end
        # 트리의 노드 구조를 저장
        # node_id: { value, left_child_id, right_child_id, status (waiting/computing/done) }
        self.tree_nodes = {}
        self.next_node_id = 0
        self.current_depth = 0
        self.max_depth = 0
        
    def generate(self):
        # INIT_CODE
        code = [
            "def find_max_divide_conquer(arr, left, right):",
            "    if left == right:",
            "        return arr[left]",
            "    ",
            "    mid = (left + right) // 2",
            "    ",
            "    max_left = find_max_divide_conquer(arr, left, mid)",
            "    max_right = find_max_divide_conquer(arr, mid + 1, right)",
            "    ",
            "    return max(max_left, max_right)"
        ]
        
        yield "INIT_CODE", code, -1, "초기화: 분할 정복 코드를 불러왔습니다."
        
        # 첫 번째 루트 노드 생성 및 시작
        root_id = self.add_node(self.start, self.end, depth=0)
        
        yield from self._recursive_find_max(self.start, self.end, root_id, 0)
        
        yield "FINISHED", self.get_state(), -1, f"완료: 배열 전체의 최댓값은 {self.tree_nodes[root_id]['val']} 입니다."

    def add_node(self, left, right, depth):
        node_id = self.next_node_id
        self.next_node_id += 1
        self.max_depth = max(self.max_depth, depth)
        
        self.tree_nodes[node_id] = {
            "id": node_id,
            "left": left,
            "right": right,
            "depth": depth,
            "val": None,
            "status": "WAITING",
            "child_l": None,
            "child_r": None,
            "is_leaf": False
        }
        return node_id

    def get_state(self, current_node_id=-1):
        # 현재 전체 트리 상태 반환
        return {
            "nodes": self.tree_nodes.copy(),
            "arr": self.arr,
            "current_node_id": current_node_id
        }

    def _recursive_find_max(self, left, right, node_id, cur_depth):
        self.tree_nodes[node_id]["status"] = "COMPUTING"
        state = self.get_state(node_id)
        yield "CALL_FUNC", state, 0, f"[호출] find_max_divide_conquer(arr, left={left}, right={right})"

        yield "CHECK_BASE", self.get_state(node_id), 1, f"[검사] left({left}) == right({right}) 인가?"
        if left == right:
            val = self.arr[left]
            self.tree_nodes[node_id]["val"] = val
            self.tree_nodes[node_id]["status"] = "DONE"
            self.tree_nodes[node_id]["is_leaf"] = True
            
            yield "BASE_CASE", self.get_state(node_id), 2, f"[Base Case] 원소가 1개 남았습니다. 값 {val} 반환"
            return val
            
        mid = (left + right) // 2
        yield "CALC_MID", self.get_state(node_id), 4, f"[계산] 분할하기 위한 중간 지점 mid = ({left}+{right})//2 = {mid}"

        # Left Child
        l_id = self.add_node(left, mid, cur_depth + 1)
        self.tree_nodes[node_id]["child_l"] = l_id
        yield "DIVIDE_LEFT", self.get_state(node_id), 6, f"[재귀 호출 - 왼쪽] 범위 {left}~{mid} 의 최댓값을 구합니다."
        max_left = yield from self._recursive_find_max(left, mid, l_id, cur_depth + 1)

        # Right Child
        r_id = self.add_node(mid + 1, right, cur_depth + 1)
        self.tree_nodes[node_id]["child_r"] = r_id
        yield "DIVIDE_RIGHT", self.get_state(node_id), 7, f"[재귀 호출 - 오른쪽] 범위 {mid+1}~{right} 의 최댓값을 구합니다."
        max_right = yield from self._recursive_find_max(mid + 1, right, r_id, cur_depth + 1)

        # Merge (Conquer)
        yield "MERGE", self.get_state(node_id), 9, f"[병합(Conquer)] 왼쪽 최댓값({max_left})과 오른쪽 최댓값({max_right}) 비교 시작"
        result = max(max_left, max_right)
        
        self.tree_nodes[node_id]["val"] = result
        self.tree_nodes[node_id]["status"] = "DONE"
        
        yield "RETURN", self.get_state(node_id), 9, f"[반환] 둘 중 큰 값인 {result} 를 반환합니다."
        
        return result

def divide_conquer_generator(arr):
    gen = DivideConquerGenerator(arr, 0, len(arr) - 1)
    return gen.generate()
