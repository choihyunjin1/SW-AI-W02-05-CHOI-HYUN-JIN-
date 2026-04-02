class PriorityQueueGenerator:
    def __init__(self, patients):
        self.patients = patients
        
    def generate(self):
        # INIT_CODE
        code = [
            "import heapq",
            "",
            "def process_emergency_room(patients):",
            "    heap = []",
            "    for name, priority in patients:",
            "        heapq.heappush(heap, (priority, name))",
            "        ",
            "    processed = []",
            "    while heap:",
            "        priority, name = heapq.heappop(heap)",
            "        processed.append(name)",
            "        print(f'처리: {name} (우선순위: {priority})')",
            "        ",
            "    return processed"
        ]
        
        yield "INIT_CODE", code, -1, "초기화: 우선순위 큐(Heap)를 기반으로 한 응급실 환자 관리 코드를 불러왔습니다."
        
        heap = []
        processed = []
        
        yield "INIT_VARS", self.get_state(heap, processed), 3, "빈 우선순위 큐(Heap) 배열을 생성합니다."
        
        # enqueue phase
        for i, (name, priority) in enumerate(self.patients):
            item = (priority, name)
            
            yield "PUSH_START", self.get_state(heap, processed, current_job=item), 5, f"환자 '{name}' (우선순위 {priority}) 데이터를 힙의 맨 끝에 추가합니다."
            heap.append(item)
            curr = len(heap) - 1
            yield "PUSH_APPEND", self.get_state(heap, processed, current_job=item, curr=curr), 5, f"'{name}' 추가 완료. 힙(최소 힙) 속성을 유지하기 위해 부모 노드들과 비교하며 위로 올립니다(Sift-Up)."
            
            # sift up logic
            while curr > 0:
                parent = (curr - 1) // 2
                yield "COMPARE_UP", self.get_state(heap, processed, current_job=item, curr=curr, parent=parent), 5, f"나({heap[curr][1]}, {heap[curr][0]})의 우선순위와 부모({heap[parent][1]}, {heap[parent][0]})를 비교합니다."
                
                if heap[curr][0] < heap[parent][0]:
                    yield "SWAP_UP", self.get_state(heap, processed, current_job=item, curr=curr, parent=parent), 5, f"내 우선순위가 더 높아 부모와 자리를 바꿉니다 (Swap)."
                    heap[curr], heap[parent] = heap[parent], heap[curr]
                    curr = parent
                    yield "SWAP_DONE", self.get_state(heap, processed, current_job=item, curr=curr), 5, f"자리를 바꾼 후 다시 부모와 비교를 준비합니다."
                else:
                    yield "STOP_UP", self.get_state(heap, processed, current_job=item, curr=curr, parent=parent), 5, f"나의 우선순위가 부모보다 낮거나 같습니다. 최소 힙 조건을 만족하므로 Sift-Up을 멈춥니다."
                    break

        yield "PUSH_DONE", self.get_state(heap, processed), 7, f"모든 대기 환자가 힙에 추가되었습니다. 가장 우선순위가 높은(값이 작은) 환자부터 처리합니다."
        
        # dequeue phase
        while heap:
            yield "POP_START", self.get_state(heap, processed), 8, f"힙에서 가장 최우선 환자인 루트 요소 '{heap[0][1]}' (우선순위: {heap[0][0]}) 를 꺼냅니다."
            
            if len(heap) == 1:
                priority, name = heap.pop()
                processed.append(name)
                yield "POP_DONE", self.get_state(heap, processed, current_job=(priority, name)), 10, f"꺼내기 완료: '{name}'"
                continue
                
            lastelt = heap.pop()
            returnitem = heap[0]
            heap[0] = lastelt
            yield "POP_REPLACE_ROOT", self.get_state(heap, processed, current_job=returnitem, curr=0), 8, f"루트를 꺼내고 힙의 가장 마지막이던 '{lastelt[1]}' 를 루트로 올립니다."
            
            # sift down logic
            curr = 0
            n = len(heap)
            while True:
                left = 2 * curr + 1
                right = 2 * curr + 2
                smallest = curr
                
                yield "COMPARE_DOWN", self.get_state(heap, processed, current_job=returnitem, curr=curr, left=left if left<n else -1, right=right if right<n else -1), 8, f"루트부터 시작하여 양쪽 자식 중 가장 우선순위가 높은 놈을 찾아 아래로 내립니다(Sift-Down)."
                
                if left < n and heap[left][0] < heap[smallest][0]:
                    smallest = left
                if right < n and heap[right][0] < heap[smallest][0]:
                    smallest = right
                    
                if smallest != curr:
                    yield "SWAP_DOWN", self.get_state(heap, processed, current_job=returnitem, curr=curr, smallest=smallest), 8, f"자식 '{heap[smallest][1]}'({heap[smallest][0]}) 의 우선순위가 더 높아 부모와 바꿉니다 (Swap)."
                    heap[curr], heap[smallest] = heap[smallest], heap[curr]
                    curr = smallest
                    yield "SWAP_DONE", self.get_state(heap, processed, current_job=returnitem, curr=curr), 8, f"자리를 바꾼 후 하위 자식들과 다시 비교를 준비합니다."
                else:
                    yield "STOP_DOWN", self.get_state(heap, processed, current_job=returnitem, curr=curr), 8, f"자식 노드들보다 내 우선순위가 높거나 같습니다. Sift-Down 완료."
                    break
                    
            processed.append(returnitem[1])
            yield "PROCESS_DONE", self.get_state(heap, processed, current_job=returnitem), 10, f"환자 '{returnitem[1]}' 처리를 위해 처리 목록에 추가합니다."
            
        yield "FINISHED", self.get_state([], processed), 13, "모든 환자가 처리되었습니다."

    def get_state(self, heap, processed, current_job=None, curr=-1, parent=-1, left=-1, right=-1, smallest=-1):
        return {
            "heap": heap.copy(),
            "processed": processed.copy(),
            "current_job": current_job,
            "curr": curr,
            "parent": parent,
            "left": left,
            "right": right,
            "smallest": smallest
        }

def priority_queue_generator(patients):
    gen = PriorityQueueGenerator(patients)
    return gen.generate()
