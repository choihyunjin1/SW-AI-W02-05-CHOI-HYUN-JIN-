class MergeSortGenerator:
    def __init__(self, arr):
        self.arr = arr.copy()
        
    def generate(self):
        # INIT_CODE
        code = [
            "def merge(arr, left, mid, right):",
            "    left_arr = arr[left:mid+1]",
            "    right_arr = arr[mid+1:right+1]",
            "    i = 0; j = 0; k = left",
            "    while i < len(left_arr) and j < len(right_arr):",
            "        if left_arr[i] <= right_arr[j]:",
            "            arr[k] = left_arr[i]",
            "            i += 1; k += 1",
            "        else:",
            "            arr[k] = right_arr[j]",
            "            j += 1; k += 1",
            "    while i < len(left_arr):",
            "        arr[k] = left_arr[i]",
            "        i += 1; k += 1",
            "    while j < len(right_arr):",
            "        arr[k] = right_arr[j]",
            "        j += 1; k += 1",
            "",
            "def merge_sort_helper(arr, left, right):",
            "    if left < right:",
            "        mid = (left + right) // 2",
            "        merge_sort_helper(arr, left, mid)",
            "        merge_sort_helper(arr, mid+1, right)",
            "        merge(arr, left, mid, right)"
        ]
        
        yield "INIT_CODE", code, -1, "초기화: 병합 정렬 코드를 불러왔습니다."
        
        yield "INIT", self.get_state(), 18, f"초기 배열 상태입니다. 병합 정렬을 시작합니다."
        yield from self._merge_sort_helper(0, len(self.arr) - 1)
        
        yield "FINISHED", self.get_state(), -1, "완료: 배열 정렬이 성공적으로 완료되었습니다."

    def get_state(self, left=-1, mid=-1, right=-1, left_arr=None, right_arr=None, i=-1, j=-1, k=-1):
        return {
            "arr": self.arr.copy(),
            "left": left,
            "mid": mid,
            "right": right,
            "left_arr": left_arr,
            "right_arr": right_arr,
            "i": i,
            "j": j,
            "k": k
        }

    def _merge_sort_helper(self, left, right):
        yield "CHECK_BASE", self.get_state(left=left, right=right), 19, f"[검사] 범위 {left}~{right} 의 크기가 1보다 큰가?"
        if left < right:
            mid = (left + right) // 2
            yield "CALC_MID", self.get_state(left=left, mid=mid, right=right), 20, f"[계산] 분할 기준점 mid = ({left}+{right})//2 = {mid}"
            
            yield "DIVIDE_LEFT", self.get_state(left=left, mid=mid, right=right), 21, f"[재귀 호출 - 왼쪽] 범위 {left}~{mid} 의 병합 정렬을 요청합니다."
            yield from self._merge_sort_helper(left, mid)
            
            yield "DIVIDE_RIGHT", self.get_state(left=left, mid=mid, right=right), 22, f"[재귀 호출 - 오른쪽] 범위 {mid+1}~{right} 의 병합 정렬을 요청합니다."
            yield from self._merge_sort_helper(mid + 1, right)
            
            yield "CALL_MERGE", self.get_state(left=left, mid=mid, right=right), 23, f"[병합 함수 호출] 정렬된 {left}~{mid} 부분과 {mid+1}~{right} 부분을 합칩니다."
            yield from self._merge(left, mid, right)

    def _merge(self, left, mid, right):
        left_arr = self.arr[left:mid+1]
        right_arr = self.arr[mid+1:right+1]
        
        yield "COPY_ARR", self.get_state(left, mid, right, left_arr, right_arr), 1, f"임시 부분 배열 left_arr={left_arr}, right_arr={right_arr} 복사"
        
        i = 0
        j = 0
        k = left
        yield "INIT_VARS", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 3, f"병합 포인터 초기화: i={i}, j={j}, 원본에 저장할 위치 k={k}"
        
        while i < len(left_arr) and j < len(right_arr):
            yield "COMPARE", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 5, f"크기 비교: left_arr[{i}]({left_arr[i]}) <= right_arr[{j}]({right_arr[j]}) 인가?"
            
            if left_arr[i] <= right_arr[j]:
                yield "MERGE_LEFT", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 6, f"왼쪽 값이 작거나 같으므로 선택"
                self.arr[k] = left_arr[i]
                yield "MOVE_POINTER_L", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 7, f"arr[{k}] 위치에 {left_arr[i]} 삽입, 포인터들 이동"
                i += 1
                k += 1
            else:
                yield "MERGE_RIGHT", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 8, f"오른쪽 값이 더 작으므로 선택"
                self.arr[k] = right_arr[j]
                yield "MOVE_POINTER_R", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 10, f"arr[{k}] 위치에 {right_arr[j]} 삽입, 포인터들 이동"
                j += 1
                k += 1
                
        # 잔여 원소 처리
        while i < len(left_arr):
            yield "REMAIN_LEFT", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 11, f"왼쪽 배열의 남은 모든 원소를 순차적으로 arr 뒷부분에 복사합니다."
            self.arr[k] = left_arr[i]
            yield "COPY_REMAIN_L", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 13, f"arr[{k}] 위치에 {left_arr[i]} 삽입"
            i += 1
            k += 1

        while j < len(right_arr):
            yield "REMAIN_RIGHT", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 14, f"오른쪽 배열의 남은 모든 원소를 순차적으로 arr 뒷부분에 복사합니다."
            self.arr[k] = right_arr[j]
            yield "COPY_REMAIN_R", self.get_state(left, mid, right, left_arr, right_arr, i, j, k), 16, f"arr[{k}] 위치에 {right_arr[j]} 삽입"
            j += 1
            k += 1

def merge_sort_generator(arr):
    gen = MergeSortGenerator(arr)
    return gen.generate()
