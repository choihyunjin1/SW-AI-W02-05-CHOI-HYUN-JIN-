def binary_search_generator(arr, target):
    # INIT code
    code = [
        "def binary_search(arr, target):",
        "    left = 0",
        "    right = len(arr) - 1",
        "    ",
        "    while left <= right:",
        "        mid = (left + right) // 2",
        "        ",
        "        if arr[mid] > target:",
        "            right = mid - 1",
        "            ",
        "        elif arr[mid] < target:",
        "            left = mid + 1",
        "        else:",
        "            return mid",
        "            ",
        "    return -1"
    ]
    
    yield "INIT_CODE", code, -1, "초기화: 이분 탐색 코드를 불러왔습니다."

    left = 0
    right = len(arr) - 1
    
    state = lambda l, r, m: {"arr": arr, "target": target, "left": l, "right": r, "mid": m}
    
    yield "INIT_VARS", state(left, right, -1), 1, "초기화: left = 0"
    yield "INIT_VARS", state(left, right, -1), 2, f"초기화: right = {right}"

    while left <= right:
        yield "LOOP_COND", state(left, right, -1), 4, f"반복문 검사: left({left}) <= right({right})"
        
        mid = (left + right) // 2
        yield "CALC_MID", state(left, right, mid), 5, f"중간 인덱스 계산: mid = ({left} + {right}) // 2 = {mid}"
        yield "COMPARE", state(left, right, mid), 7, f"비교: arr[{mid}]({arr[mid]}) > target({target}) 인가?"
        
        if arr[mid] > target:
            right = mid - 1
            yield "UPDATE_RIGHT", state(left, right, mid), 8, f"target이 더 작으므로 탐색 범위를 왼쪽으로 좁힙니다. right = {right}"
        else:
            yield "COMPARE", state(left, right, mid), 10, f"비교: arr[{mid}]({arr[mid]}) < target({target}) 인가?"
            if arr[mid] < target:
                left = mid + 1
                yield "UPDATE_LEFT", state(left, right, mid), 11, f"target이 더 크므로 탐색 범위를 오른쪽으로 좁힙니다. left = {left}"
            else:
                yield "FOUND", state(left, right, mid), 13, f"찾았습니다! 값을 반환합니다. 결과 인덱스: {mid}"
                return
    
    yield "NOT_FOUND", state(left, right, -1), 15, "탐색 실패: target 값을 배열에서 찾지 못했습니다."
