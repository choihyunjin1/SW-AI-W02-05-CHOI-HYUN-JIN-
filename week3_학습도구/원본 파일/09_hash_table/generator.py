class HashTableGenerator:
    def __init__(self, data_pairs, search_names):
        self.data_pairs = data_pairs 
        self.search_names = search_names
        self.num_buckets = 5
        self.buckets = [[] for _ in range(self.num_buckets)]
        
    def _my_hash(self, key):
        # 파이썬의 hash() 대신 시각화를 위해 간단한 ASCII 합 해시함수를 사용
        return sum(ord(c) for c in key)
        
    def generate(self):
        code = [
            "def manage_grades(students):",
            "    average = sum(students.values()) / len(students)",
            "    top_student = max(students, key=students.get)",
            "    top_score = students[top_student]",
            "    return average, top_student, top_score",
            "",
            "def find_student_score(students, name):",
            "    if name in students:",
            "        return students[name]",
            "    return None"
        ]
        
        yield "INIT_CODE", code, -1, "초기화: 학생 성적 관리 코드를 불러왔습니다."
        
        yield "INIT_VARS", self.get_state(), -1, "시작 전: 파이썬 딕셔너리(dict)가 내부적으로 사용하는 해시 테이블 구조를 모사하여 시각화합니다. 빈 버킷(Bucket) 5개를 생성합니다."

        ## 1. 데이터 삽입 페이즈 (Dictionary 생성 과정 시뮬레이션)
        for (name, score) in self.data_pairs:
            yield "INSERT_START", self.get_state(curr_name=name, curr_val=score), -1, f"딕셔너리에 데이터 삽입: ['{name}'] = {score}"
            
            h_val = self._my_hash(name)
            yield "HASH_CALC", self.get_state(curr_name=name, curr_val=score, h_val=h_val), -1, f"해시 함수(간이) 적용: Hash('{name}') = sum(ASCII) = {h_val}"
            
            bucket_idx = h_val % self.num_buckets
            yield "MOD_CALC", self.get_state(curr_name=name, curr_val=score, h_val=h_val, bucket_idx=bucket_idx), -1, f"버킷 인덱스 맵핑: {h_val} % {self.num_buckets} (버킷 개수) = {bucket_idx}"
            
            # 저장 전 충돌 확인
            collision = len(self.buckets[bucket_idx]) > 0
            if collision:
                yield "COLLISION", self.get_state(curr_name=name, curr_val=score, h_val=h_val, bucket_idx=bucket_idx), -1, f"충돌 발생! {bucket_idx}번 버킷에 이미 데이터가 있습니다. 해당 버킷 리스트 끝에 체이닝(Chaining)으로 연결합니다."
            
            self.buckets[bucket_idx].append((name, score))
            yield "INSERT_DONE", self.get_state(curr_name=name, curr_val=score, h_val=h_val, bucket_idx=bucket_idx), -1, f"{bucket_idx}번 버킷에 ('{name}', {score}) 데이터 저장을 완료했습니다."
            
        yield "SETUP_DONE", self.get_state(), 1, "딕셔너리 생성이 완료되었습니다. 이제 평균과 최고점 학생을 찾는 코드를 실행합니다."
        
        ## 2. 평균 점수 계산 페이즈
        total_sum = sum(score for name, score in self.data_pairs)
        total_len = len(self.data_pairs)
        avg = total_sum / total_len
        yield "CALC_AVG", self.get_state(res_avg=avg), 1, f"평균 점수 계산 완료: sum({total_sum}) / len({total_len}) = {avg}"
        
        ## 3. 최고점 찾기 페이즈 
        top_name = None
        top_score = -1
        for name, score in self.data_pairs:
            if score > top_score:
                top_name = name
                top_score = score
                
        yield "CALC_MAX_NAME", self.get_state(res_avg=avg, res_top_name=top_name), 2, f"순회를 거쳐 최고 점수 학생을 찾았습니다: '{top_name}'"
        yield "CALC_MAX_SCORE", self.get_state(res_avg=avg, res_top_name=top_name, res_top_score=top_score), 3, f"최고 점수 학생의 점수를 조회합니다: {top_score}"
        
        yield "RETURN_MGMT", self.get_state(res_avg=avg, res_top_name=top_name, res_top_score=top_score), 4, f"학생 성적 관리 작업 완료 반환. (평균: {avg}, 최고자: {top_name}, 최고점: {top_score})"
        
        ## 4. 탐색 (Search) 페이즈
        for s_name in self.search_names:
            yield "SEARCH_START", self.get_state(s_name=s_name), 7, f"조회 작업: '{s_name}' 학생의 점수 찾기를 시작합니다."
            
            h_val = self._my_hash(s_name)
            yield "SEARCH_HASH", self.get_state(s_name=s_name, h_val=h_val), -1, f"해시 함수(간이) 재적용: Hash('{s_name}') = {h_val}"
            
            bucket_idx = h_val % self.num_buckets
            yield "SEARCH_IDX", self.get_state(s_name=s_name, h_val=h_val, bucket_idx=bucket_idx), 7, f"버킷 인덱스 계산: {h_val} % {self.num_buckets} = {bucket_idx}. {bucket_idx}번 버킷으로 직행하여 검색합니다! (O(1) 속도의 비결)"
            
            found = False
            found_score = None
            chain_idx = 0
            for (k, v) in self.buckets[bucket_idx]:
                yield "SEARCH_CHAIN", self.get_state(s_name=s_name, h_val=h_val, bucket_idx=bucket_idx, chain_idx=chain_idx, curr_name=k), 7, f"{bucket_idx}번 버킷 요소 검사: Key가 '{s_name}'와 일치하는가? -> 비교 대상: '{k}'"
                if k == s_name:
                    found = True
                    found_score = v
                    yield "SEARCH_FOUND", self.get_state(s_name=s_name, h_val=h_val, bucket_idx=bucket_idx, chain_idx=chain_idx, curr_name=k, curr_val=v), 8, f"일치 항목 발견! 값을 반환합니다: {v}"
                    break
                chain_idx += 1
                
            if not found:
                yield "SEARCH_NOT_FOUND", self.get_state(s_name=s_name, h_val=h_val, bucket_idx=bucket_idx), 9, f"해당 버킷 내에 일치하는 Key가 없습니다. 탐색 실패, None을 반환합니다."
                
        yield "FINISHED", self.get_state(), -1, "해시 테이블의 요소를 삽입하고 O(1)에 가깝게 바로 찾아가는 과정을 모두 확인했습니다."
                
        
    def get_state(self, curr_name=None, curr_val=None, h_val=None, bucket_idx=None, chain_idx=None, res_avg=None, res_top_name=None, res_top_score=None, s_name=None):
        import copy
        return {
            "buckets": copy.deepcopy(self.buckets),
            "curr_name": curr_name,
            "curr_val": curr_val,
            "h_val": h_val,
            "bucket_idx": bucket_idx,
            "chain_idx": chain_idx,
            "res_avg": res_avg,
            "res_top_name": res_top_name,
            "res_top_score": res_top_score,
            "s_name": s_name
        }

def hash_table_generator(data_pairs, search_names):
    gen = HashTableGenerator(data_pairs, search_names)
    return gen.generate()
