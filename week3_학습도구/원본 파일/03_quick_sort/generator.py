# quick_sort_generator.py
# 퀵 정렬 실행 과정을 단계별로 시각화하기 위해 상태를 yield 하는 제너레이터입니다.

QUICK_SORT_CODE = [
    "def partition(arr, low, high):",                     # 0
    "    pibut = arr[high]",                              # 1
    "    i = low - 1",                                    # 2
    "    ",                                               # 3
    "    for j in range(low, high):",                     # 4
    "        if arr[j] <= pibut:",                        # 5
    "            i += 1",                                 # 6
    "            tmp = arr[i]",                           # 7
    "            arr[i] = arr[j]",                        # 8
    "            arr[j] = tmp",                           # 9
    "",                                                   # 10
    "    tmp = arr[high]",                                # 11
    "    arr[high] = arr[i+1]",                           # 12
    "    arr[i+1] = tmp",                                 # 13
    "    return i + 1",                                   # 14
    "",                                                   # 15
    "def quick_sort_helper(arr, low, high):",             # 16
    "    if low < high:",                                 # 17
    "        p = partition(arr, low, high)",              # 18
    "        quick_sort_helper(arr, low, p - 1)",         # 19
    "        quick_sort_helper(arr, p + 1, high)",        # 20
    "",                                                   # 21
    "def quick_sort(arr):",                               # 22
    "    quick_sort_helper(arr, 0, len(arr) - 1)",        # 23
    "    return arr"                                      # 24
]

def make_state(arr, low=-1, high=-1, i=-1, j=-1, pibut=None, p=-1):
    return {
        "arr": list(arr),
        "low": low,
        "high": high,
        "i": i,
        "j": j,
        "pibut": pibut,
        "p": p
    }

def quick_sort_generator(arr_input):
    yield "INIT_CODE", QUICK_SORT_CODE, -1, "초기화 되었습니다."
    
    arr = list(arr_input)
    
    yield "START", make_state(arr), 22, "quick_sort 함수 호출"
    yield "CALL", make_state(arr), 23, f"quick_sort_helper 호출: arr={arr}, low=0, high={len(arr)-1}"
    
    yield from _quick_sort_helper_gen(arr, 0, len(arr) - 1)
    
    yield "FINISH", make_state(arr), 24, "최종 정렬 완료"
    return arr

def _quick_sort_helper_gen(arr, low, high):
    yield "FUNC_CALL", make_state(arr, low=low, high=high), 16, f"quick_sort_helper(arr, {low}, {high}) 호출"
    yield "CHECK", make_state(arr, low=low, high=high), 17, f"low({low}) < high({high}) 비교"
    if low < high:
        yield "CALL_PARTITION", make_state(arr, low=low, high=high), 18, f"partition(arr, {low}, {high}) 함수 호출"
        
        # partition inlined equivalent for generator
        p = yield from _partition_gen(arr, low, high)
        
        yield "RECURSIVE_LEFT", make_state(arr, low=low, high=high, p=p), 19, f"왼쪽 부분 정렬: quick_sort_helper(arr, {low}, {p-1})"
        yield from _quick_sort_helper_gen(arr, low, p - 1)
        
        yield "RECURSIVE_RIGHT", make_state(arr, low=low, high=high, p=p), 20, f"오른쪽 부분 정렬: quick_sort_helper(arr, {p+1}, {high})"
        yield from _quick_sort_helper_gen(arr, p + 1, high)
        
    else:
        yield "RETURN", make_state(arr, low=low, high=high), 17, f"low({low}) >= high({high}) 이므로 종료"

def _partition_gen(arr, low, high):
    yield "PARTITION_CALL", make_state(arr, low=low, high=high), 0, f"partition 시작 (범위: {low}~{high})"
    pibut = arr[high]
    yield "SET_PIVOT", make_state(arr, low=low, high=high, pibut=pibut), 1, f"피벗(pibut) 설정: arr[{high}] = {pibut}"
    
    i = low - 1
    yield "SET_I", make_state(arr, low=low, high=high, pibut=pibut, i=i), 2, f"i 초기화: {i} (작은 원소들의 마지막 인덱스)"
    
    yield "START_LOOP", make_state(arr, low=low, high=high, pibut=pibut, i=i), 4, f"j를 {low}부터 {high-1}까지 순회 시작"
    for j in range(low, high):
        yield "LOOP_J", make_state(arr, low=low, high=high, pibut=pibut, i=i, j=j), 4, f"현재 j: {j}"
        
        yield "COMPARE", make_state(arr, low=low, high=high, pibut=pibut, i=i, j=j), 5, f"arr[{j}]({arr[j]}) <= pibut({pibut}) 비교"
        if arr[j] <= pibut:
            i += 1
            yield "INC_I", make_state(arr, low=low, high=high, pibut=pibut, i=i, j=j), 6, f"조건 만족! i를 1 증가 -> i={i}"
            
            yield "SWAP_PREP", make_state(arr, low=low, high=high, pibut=pibut, i=i, j=j), 7, f"교환 준비: arr[{i}]({arr[i]}) <-> arr[{j}]({arr[j]})"
            
            tmp = arr[i]
            arr[i] = arr[j]
            yield "SWAP_1", make_state(arr, low=low, high=high, pibut=pibut, i=i, j=j), 8, f"arr[{i}]에 arr[{j}] 값 대입"
            
            arr[j] = tmp
            yield "SWAP_2", make_state(arr, low=low, high=high, pibut=pibut, i=i, j=j), 9, f"arr[{j}]에 tmp 대입 (교환 완료)"
        else:
            yield "NO_SWAP", make_state(arr, low=low, high=high, pibut=pibut, i=i, j=j), 5, f"조건 불만족. 아무 작업 없이 다음 루프로 이동."

    yield "PLACE_PIVOT_PREP", make_state(arr, low=low, high=high, pibut=pibut, i=i), 11, f"피벗을 올바른 위치({i+1})에 배치 준비"
    tmp = arr[high]
    arr[high] = arr[i+1]
    yield "PLACE_PIVOT_1", make_state(arr, low=low, high=high, pibut=pibut, i=i), 12, f"arr[{high}]에 arr[{i+1}]({arr[i+1]}) 대입"
    
    arr[i+1] = tmp
    yield "PLACE_PIVOT_2", make_state(arr, low=low, high=high, pibut=pibut, i=i), 13, f"arr[{i+1}]에 피벗 값({tmp}) 대입 (피벗 제자리 찾음)"
    
    yield "RETURN_PIVOT", make_state(arr, low=low, high=high, pibut=pibut, i=i, p=i+1), 14, f"새로운 피벗 위치 p = {i+1} 반환"
    return i + 1
